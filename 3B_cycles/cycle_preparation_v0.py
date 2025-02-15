#!/usr/bin/env python
# coding: utf-8
#Cycle_preparation aims at preparing existing cycle before computing the calculation of cycle variables and behavior parameters. It takes into argument a cycle (csv format) and return the theoretical path cycle and the list of all extrema. 
# # IMPORTATION 

# In[44]:


from pylab import *
import csv
import numpy as np
from scipy.signal import argrelextrema


# # Mise en forme cycle

# In[45]:


def cycle_opening (nom_fichier):
  with open(nom_fichier) as file_name:
    file_read = csv.reader(file_name)

    array = list(file_read)
 
  nom_cycle=array[0][0]
  suite=array[1:]
  mon_cycle=[0]*len(suite)
  for k in range (0, len(suite)):
    mon_cycle[k]=float(suite[k][0])/3.6 #fichier avec données en kmh
  return mon_cycle


# In[46]:


def t_to_d (cycle):
    d=[0]
    distance=0
    temps=len(cycle)
    for k in range (1,temps):
        v0=cycle[k-1]
        v1=cycle[k]
        distance+=(v1+v0)/2
        d+=[distance]
    d=np.array(d)
    return d


# ## Création path

# In[47]:


def extrema_standard(lst):
    arr = np.array(lst)

    # Find indices of local maxima and minima.
    maxima_indices = argrelextrema(arr, np.greater)[0]
    minima_indices = argrelextrema(arr, np.less)[0]

    # Find indices where the values are constant and only keep the beginning and the end indice of the moment where it is constant.
    diff_arr = np.diff(arr)
    constant_start_indices = np.where(diff_arr[1:] == 0)[0]
    constant_end_indices=np.where(diff_arr[:-1] == 0)[0]
    unique_1 = np.setdiff1d(constant_start_indices, constant_end_indices)
    unique_2 = np.setdiff1d(constant_end_indices, constant_start_indices)

    indice_list = np.concatenate(([0,len(arr)-1],maxima_indices,minima_indices,unique_1+1, unique_2+1))
    indice_list.sort()
    
    # Create a list of tuples with value, position, and type
    extrema_list = np.array([(arr[i]) for i in indice_list])

    return extrema_list,indice_list


# In[48]:


def extrema_smooth (lst,limit):
    arr = np.array(lst)

    list_D=np.array(t_to_d(lst))

    # Find indices of local maxima and minima.
    maxima_indices = argrelextrema(arr, np.greater)[0]
    minima_indices = argrelextrema(arr, np.less)[0]

    # Find indices where the values are constant and only keep the beginning and the end indice of the moment where it is constant.
    diff_arr = np.diff(arr)
    zeros=np.array(np.where(np.diff(arr)==0))
    zeros_add=zeros+1
    unique_1_a = np.setdiff1d(zeros, zeros_add)
    unique_2_a = np.setdiff1d(zeros_add, zeros)
    
    constant_start_indices = np.where(diff_arr[1:] == 0)[0]
    constant_end_indices=np.where(diff_arr[:-1] == 0)[0]
    unique_1 = np.setdiff1d(constant_start_indices, constant_end_indices)
    unique_2 = np.setdiff1d(constant_end_indices, constant_start_indices)
    


    indice_list = np.concatenate(([0,len(arr)-1],maxima_indices,minima_indices,unique_1+1, unique_2+1))
    indice_list.sort()
    
    extrema_list = arr[indice_list]
    list_incident_D = list_D[indice_list]

    
    ########### First rule : braking with low braking force are neglected - considering that this is rather driver behavior than path induce #########
    
    values = extrema_list
    diff_pos=np.diff(list_incident_D)
    
    values_2=values*values/2
    values_2_pos=np.diff(values_2)
    
    
    force = (values_2_pos/diff_pos)
    
    diff_values=np.diff(values)
    incident_pos = np.where(diff_values < 0)[0]
    braking_distance=diff_pos[incident_pos]
    braking_force = -values_2_pos[values_2_pos < 0] / braking_distance
    
    indice_to_smooth=np.where((0>force) & (force>-limit))[0]



       
    indice_to_erase=[]
    for i in indice_to_smooth:
        j=1
            
        if values[i+1]==values[i+2]:
            indice_to_erase+=[i+1]
            j+=1
        if (values[i]>values[i+j+1]) & (values[i+1]<values[i+j+1]):
            indice_to_erase+=[i+j]
            j+=1
        
        moyenne=np.mean(arr[indice_list[i]:indice_list[i+j]])
        if values[i]==values[i-1]:
            values[i-1]=moyenne
        values[i]=moyenne
        values[i+j]=moyenne
        

    
    values=np.delete(values,indice_to_erase)
    indice_list=np.delete(indice_list,indice_to_erase)
    
    
    ########### Second rule : gear change during acceleration #########
        #We seek for incident during acceleration phase that only last 1 or 2 seconds, which corresponds to a gear shift.
    extrema_duration=np.diff(indice_list)

    diff_values=np.diff(values)
    incident_pos = np.where(diff_values < 0)[0]
    
    short_incident=incident_pos[np.where((extrema_duration[incident_pos]<=2))[0]]
    
    gear_change=incident_pos[np.where((diff_values[short_incident-1]>0) & (extrema_duration[short_incident-1]>3) & (diff_values[short_incident+1]>0) & (extrema_duration[short_incident+1]>3))[0]]
    
    indice_to_erase=[gear_change,gear_change+1]

    values=np.delete(values,indice_to_erase)
    indice_list=np.delete(indice_list,indice_to_erase)

    return values,indice_list
        
    
    
    
    


# In[49]:


def extrema(lst,limit=0):
    if limit==0:
        return extrema_standard(lst)
    else:
        return extrema_smooth(lst,limit)


# In[52]:


def cycle_path(extrema_list):
    
    values = np.array(extrema_list[0])
    positions = np.array(extrema_list[1],dtype=int)

    next_values = np.roll(values, -1)
    next_positions = np.roll(positions, -1)

    cycle_values = np.maximum(values, next_values)
    cycle_lengths = (next_positions - positions - 1)
    
    cycle=[]
    for k in range(len(values)-1):
        cycle.append(values[k])
        cycle+= [cycle_values[k]]*cycle_lengths[k]
    cycle.append(values[-1])
    cycle=np.array(cycle)
    return cycle

# In[53]:

def idle_time (cycle):
    cycle=np.array(cycle)
    cycle_roll=np.roll(cycle,-1)
    idle=np.where((cycle==0)&(cycle_roll==0))[0]
    return len(idle)-1


# In[54]:


def cycle_prepared(nom_fichier,limit=0):
    nom=nom_fichier[:-4]
    cycle=cycle_opening(nom_fichier)
    t_idle=idle_time(cycle)
    list_D=t_to_d(cycle)
    ext=extrema(cycle,limit)
    path=cycle_path(ext)
    cycle=np.array(cycle)
    return [nom,list_D,ext,path,cycle,t_idle]
