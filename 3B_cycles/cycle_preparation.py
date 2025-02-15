#!/usr/bin/env python
# coding: utf-8
"""Cycle_preparation aims at preparing the path target speed from an existing driving cycle."""
# In[1]:


from pylab import *
import csv
import numpy as np
from scipy.signal import argrelextrema


# In[2]:


def cycle_opening(file_name):
    """
    Open and read a driving cycle file, extracting and converting speed data.

    Parameters:
    file_name (str): Path to the CSV file containing the cycle data.

    Returns:
    list: A list of speed values (converted from km/h to m/s): the driving cycle.
    """
    # Read the file and extract data
    with open(file_name, 'r') as file:
        file_reader = csv.reader(file)
        data = list(file_reader)

    # Extract the cycle name and speed data
    cycle_name = data[0][0]
    speed_data_raw = data[1:]

    # Convert speed values from km/h to m/s
    speed_cycle = [float(row[0]) / 3.6 for row in speed_data_raw]

    return speed_cycle


# In[3]:


def t_to_d(cycle):
    """
    Convert a time series of speed values to a cumulative distance array.

    Parameters:
    cycle (list or array): Speed values (m/s) over time.

    Returns:
    array: Cumulative distance at each time step.
    """
    # Initialize distance array
    distance = 0
    distances = [0]

    # Calculate cumulative distance using trapezoidal integration
    for k in range(1, len(cycle)):
        v0 = cycle[k - 1]
        v1 = cycle[k]
        distance += (v1 + v0) / 2  # Trapezoidal area
        distances.append(distance)

    return np.array(distances)


# In[4]:


def extrema_standard(lst):
    """
    Identify local maxima, minima, and points of constant values in a list.

    Parameters:
    lst (list or array): Input list of values.

    Returns:
    tuple:
        - extrema_list (array): Array of extrema values.
        - indice_list (array): Array of indices corresponding to the extrema.
    """
    arr = np.array(lst)

    # Find indices of local maxima and minima
    maxima_indices = argrelextrema(arr, np.greater)[0]
    minima_indices = argrelextrema(arr, np.less)[0]

    # Identify constant regions by comparing differences between consecutive values
    diff_arr = np.diff(arr)
    constant_start_indices = np.where(diff_arr[1:] == 0)[0]
    constant_end_indices=np.where(diff_arr[:-1] == 0)[0]

    # Filter the constant regions to get only unique start and end points
    unique_1 = np.setdiff1d(constant_start_indices, constant_end_indices)
    unique_2 = np.setdiff1d(constant_end_indices, constant_start_indices)



    # Combine all indices (maxima, minima, constant regions, boundaries) and include boundary points (0 and len(arr) - 1) as extrema
    indice_list = np.concatenate(([0,len(arr)-1],maxima_indices,minima_indices,unique_1+1, unique_2+1))
    indice_list.sort()
    
    # Extract the extrema values corresponding to the indices
    extrema_list = np.array([(arr[i]) for i in indice_list])
    

    return extrema_list, indice_list


# In[5]:


def extrema_smooth(lst, limit):
    """
    Identify and smooth extrema points in a list with rules for neglecting low braking forces
    and detecting gear changes during acceleration phases.

    Parameters:
    lst (list or array): Input list of values (e.g., speed values).
    limit (float): Threshold for neglecting low braking forces.

    Returns:
    tuple:
        - values (array): Smoothed list of extrema values.
        - indice_list (array): List of indices corresponding to the smoothed extrema.
    """
    arr = np.array(lst)
    list_D=np.array(t_to_d(lst))

    # Find indices of local maxima and minima
    maxima_indices = argrelextrema(arr, np.greater)[0]
    minima_indices = argrelextrema(arr, np.less)[0]

    # Identify constant regions by comparing differences between consecutive values
    diff_arr = np.diff(arr)
    constant_start_indices = np.where(diff_arr[1:] == 0)[0]
    constant_end_indices=np.where(diff_arr[:-1] == 0)[0]

    # Filter the constant regions to get only unique start and end points
    unique_1 = np.setdiff1d(constant_start_indices, constant_end_indices)
    unique_2 = np.setdiff1d(constant_end_indices, constant_start_indices)



    # Combine all indices (maxima, minima, constant regions, boundaries) and include boundary points (0 and len(arr) - 1) as extrema
    indice_list = np.concatenate(([0,len(arr)-1],maxima_indices,minima_indices,unique_1+1, unique_2+1))
    indice_list.sort()
    
    # Extract the extrema values corresponding to the indices
    extrema_list = np.array([(arr[i]) for i in indice_list])
    list_incident_D = list_D[indice_list]

    
   # Rule 1: Neglect low braking forces
    values = extrema_list
    diff_pos = np.diff(list_incident_D)
    values_2 = values ** 2 / 2
    values_2_pos = np.diff(values_2)

    force = values_2_pos / diff_pos
    incident_pos = np.where(np.diff(values) < 0)[0]
    braking_distance = diff_pos[incident_pos]
    braking_force = -values_2_pos[values_2_pos < 0] / braking_distance

    indices_to_smooth = np.where((force < 0) & (force > -limit))[0]

    indices_to_erase = []
    for i in indices_to_smooth:
        j = 1

        # Check if values are constant and smooth the region
        if values[i + 1] == values[i + 2]:
            indices_to_erase.append(i + 1)
            j += 1
        if (values[i] > values[i + j + 1]) and (values[i + 1] < values[i + j + 1]):
            indices_to_erase.append(i + j)
            j += 1

        # Smooth the values in the region
        mean_value = np.mean(arr[indice_list[i]:indice_list[i + j]])
        if values[i] == values[i - 1]:
            values[i - 1] = mean_value
        values[i] = mean_value
        values[i + j] = mean_value

    # Remove smoothed indices
    values = np.delete(values, indices_to_erase)
    indice_list = np.delete(indice_list, indices_to_erase)

    
    # Rule 2: Detect gear changes during acceleration phases
   
    extrema_duration=np.diff(indice_list)
    diff_values=np.diff(values)
    
    # Identify short incidents lasting 1-2 seconds
    incident_pos = np.where(diff_values < 0)[0]
    short_incident=incident_pos[np.where((extrema_duration[incident_pos]<=2))[0]]
    
    # Detect gear change patterns
    gear_change=incident_pos[np.where((diff_values[short_incident-1]>0) & (extrema_duration[short_incident-1]>3) & (diff_values[short_incident+1]>0) & (extrema_duration[short_incident+1]>3))[0]]
    
    # Remove gear change-related extrema
    indice_to_erase=[gear_change,gear_change+1]

    values=np.delete(values,indice_to_erase)
    indice_list=np.delete(indice_list,indice_to_erase)

    return values,indice_list


        
    
    
    
    


# In[6]:


def extrema(lst, limit=0):
    """
    Identify extrema points (local maxima, minima, and constant regions) in a list.
    Apply smoothing rules if a limit is provided.

    Parameters:
    lst (list or array): Input list of values.
    limit (float): Threshold for smoothing based on low braking forces. 
                   If set to 0, standard extrema detection is applied.

    Returns:
    tuple:
        - values (array): List of extrema values.
        - indices (array): Corresponding indices of the extrema.
    """
    if limit == 0:
        return extrema_standard(lst)
    else:
        return extrema_smooth(lst, limit)


# In[7]:


def cycle_path(extrema_list):
    """
    Reconstruct the path of a cycle based on a list of extrema values and positions.

    Parameters:
    extrema_list (tuple): Contains two arrays:
                          - extrema_list[0]: Array of extrema values.
                          - extrema_list[1]: Array of corresponding positions.

    Returns:
    array: Reconstructed cycle path.
    """
    values = np.array(extrema_list[0])
    positions = np.array(extrema_list[1], dtype=int)

    # Calculate next values and positions
    next_values = np.roll(values, -1)
    next_positions = np.roll(positions, -1)

    # Determine cycle values and segment lengths
    cycle_values = np.maximum(values, next_values)
    segment_lengths = next_positions - positions - 1

    # Reconstruct the cycle path
    cycle = []
    for k in range(len(values) - 1):
        cycle.append(values[k])
        cycle.extend([cycle_values[k]] * segment_lengths[k])
    
    cycle.append(values[-1])
    
    return np.array(cycle)


# In[8]:


def idle_time(cycle):
    """
    Calculate the duration of idle time in a cycle, where idle time is defined as consecutive zero values.

    Parameters:
    cycle (list or array): Array of speed values (e.g., in m/s).

    Returns:
    int: Duration of idle time (number of time steps where the cycle remains idle).
    """
    cycle = np.array(cycle)

    # Identify where the cycle is continuously idle (speed is zero)
    idle_segments = np.where((cycle == 0) & (np.roll(cycle, -1) == 0))[0]

    # Return the number of idle time steps, minus one to correct for roll overlap
    return len(idle_segments) - 1


# In[9]:


def cycle_prepared(file_name, limit=0):
    """
    Prepare the path target speed from a driving cycle.
    1) extracting relevant information such as idle time, distance, extrema. 
    2) Optional step: smoothing the path with limit of braking deceleration and gear shifting.
    3) reconstruct the target speed from the extracted information

    Parameters:
    file_name (str): Path to the cycle file.
    limit (float): Threshold for smoothing extrema. If set to 0, no smoothing is applied.

    Returns:
    list: A list containing:
          - Cycle name (str)
          - Distance array (array)
          - Extrema data (tuple of values and positions)
          - Target speed (array)
          - Original cycle data (array)
          - Idle time (int)
    """
    # Extract cycle name from the file name
    cycle_name = file_name[:-4]

    # Open and process the cycle data
    cycle = cycle_opening(file_name)
    t_idle = idle_time(cycle)

    # Convert cycle data to distance and identify extrema
    list_D = t_to_d(cycle)
    ext = extrema(cycle, limit)

    # Generate the cycle path
    path = cycle_path(ext)

    return [cycle_name, list_D, ext, path, cycle, t_idle]

