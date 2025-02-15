#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np


# In[2]:


### Physical parameters ###
g=9.81
rho_air=1.2
fuel=32.3
Na_max=550
B_lim=1.3


# In[4]:


def EC_th (body,engine,trans,path,driver):
    
    ### inventories ###
    M_body,r0,Cd,A,Iw,Rw,transf,Pacc,M_eq,Cd_eq=body
    P_max,ne,D,fmep0,p0,Q0,N_idle,cs,stop_start=engine
    ntr,a_tr,S,Ne=trans
    J3p,K1p,K2p,rate_acc,J0p,H,w,urban,dist,t_idle=path
    B,mu_v,mu_a,mu_N,M_payload=driver
    LHV=fuel

    
    ### calculated parameters ###
    M_tot=M_body+M_payload+M_eq
    Cd=Cd*Cd_eq
    PaM=P_max/M_tot*mu_a
    sigma_t=transf/Rw
    conv=LHV*10
    
    ### computed parameters for integration model ###
    
    K1=K1p*mu_v*mu_v
    K2=K2p*mu_v*mu_v*mu_v
    ta=1/PaM*K1
    da=1/PaM*K2
    
    Nc=Ne*np.pi/30*mu_N
    N_idle=N_idle*np.pi/30
    Na=N_idle+np.sqrt(mu_a)*Na_max
    
    if Na<Nc:
        Na=Nc
    
    
    ### integration variables ###
    J1=1-K1/B
    J1_cruise=1-K1/B-da
    J0_cruise=J0p/mu_v*J1_cruise
    J3_cruise=mu_v*mu_v*J3p*J1_cruise
    J0=J0p/mu_v*(J1-da*(1-1/rate_acc))
    J3=mu_v*mu_v*J3p*(J1-da*(1-rate_acc*rate_acc))
    Chi1=urban*Nc*(J0_cruise)+(1-urban)*sigma_t*J1_cruise+Na*ta
    Chi3=urban*Nc*Nc*Nc*J0_cruise+(1-urban)*sigma_t*sigma_t*sigma_t*J3_cruise+Na*Na*Na*ta
    
    
    ### External forces computation ###
    
    rolling=r0*M_tot*g*J1/conv/ne/ntr
    drag=0.5*rho_air*Cd*A*J3/conv/ne/ntr
    inertia=(M_tot+4*Iw/Rw/Rw)*K1/conv/ne/ntr
    grade=M_tot*g*H/conv/ne/ntr
    wind=0.5*rho_air*Cd*A*w*w*J1/conv/ne/ntr
    
    ### powertrain losses computation ###
    
    friction=fmep0/(4*np.pi)*D*Chi1/conv/ne
    pumping=p0/(4*np.pi)*D*Chi3/conv/ne
    thermal=Q0*D*J0/conv/ne
    cold_engine=cs*P_max/conv/dist
    accessories=Pacc*(J0p+t_idle)/conv/ne
    transmission=a_tr*P_max*Chi1/conv/ntr/ne
    synchronization=urban*S/conv/ne
    idling=(fmep0/(4*np.pi)*D*N_idle*t_idle/conv/ne+p0/(4*np.pi)*D*N_idle*N_idle*N_idle*t_idle/conv/ne+Q0*D*t_idle/conv/ne)*stop_start
    
    
    ### Final EC ###
    EC=rolling+drag+inertia+grade+wind+friction+pumping+thermal+accessories+transmission+synchronization+cold_engine+idling
    
    ### Aggregated efficiencies ###
    engine_losses=friction+pumping+thermal+cold_engine+idling+accessories
    transmission_losses=transmission+synchronization
    nop_engine=ne*(1-engine_losses/(ntr*EC-transmission_losses))
    nop_transmission=ntr*(1-(transmission_losses)/EC)
    nop=nop_engine*nop_transmission


    return EC,[rolling,drag,inertia,grade,wind,friction,pumping,thermal,accessories,transmission,synchronization,cold_engine,idling],[nop_engine,nop_transmission,nop]
    
    
    


# In[5]:


def EC_el (body,engine,trans,path,driver,battery):
    
    ### inventories ###
    M_body,r0,Cd,A,Iw,Rw,transf,Pacc,M_eq,Cd_eq=body
    P_e,Tmax,ne,alpha,epsilon,betha=engine
    a_tr,ntr=trans
    J3p,K1p,K2p,rate_acc,J0p,H,w,urban,dist,t_idle=path
    B,mu_v,mu_a,mu_N,M_payload=driver
    R_bat,U_bat,M_bat,n_bat=battery

    
    
    ### calculated parameters ###
    
    conv=36
    M_tot=M_body+M_payload+M_eq+M_bat
    PaM=P_e/M_tot*mu_a
    P_a=P_e*mu_a
    Cd=Cd*Cd_eq
    sigma_t=transf/Rw
    
    
    
    ## Regenerative Braking Efficiency ##
    if B>B_lim/2:
        nregen=1-(2*B-B_lim)*(2*B-B_lim)/(4*B*B)
    else:
        nregen=1

    
    ### computed parameters for integration model ###
    K1=K1p*mu_v*mu_v
    K2=K2p*mu_v*mu_v*mu_v
    ta=1/PaM*K1
    da=1/PaM*K2
    C2=(Tmax)*(mu_a*Tmax)*ta
    
    
    ### integration variables ###
    
    J1=1-K1/B*(1-rate_acc*rate_acc)
    J1a=J1-da*(1-rate_acc*rate_acc)
    J0=J0p/mu_v*(1-(K1/B-da)*(1-1/rate_acc))
    J3=mu_v*mu_v*J3p*(1-K1/B*(1-rate_acc*rate_acc)-da*(1-rate_acc*rate_acc))
    Chi1=sigma_t
    
    
    
    ### External forces computation ###
    rolling=r0*M_tot*g/conv/ne/ntr/n_bat
    drag=0.5*rho_air*Cd*A*J3/conv/ne/ntr/n_bat
    inertia=(M_tot+4*Iw/Rw*Rw)*K1/conv/ne/ntr*(1-nregen)/n_bat
    grade=M_tot*g*H/conv/ne/ntr/n_bat
    wind=0.5*rho_air*Cd*A*w*w/conv/ne/ntr/n_bat
    
    ### powertrain losses computation ###
    friction=alpha*Chi1/conv/ne/n_bat
    copper=epsilon*C2/conv/ne/n_bat
    converter=betha*J0/conv/ne/n_bat
    accessories=Pacc*(J0p+t_idle)/conv/ne/n_bat
    transmission=a_tr*P_e*Chi1/conv/ntr/ne/n_bat 
    
    ### battery losses computation ###
    P2_cruise=1/J0*((rolling+drag+grade+wind+friction+copper+converter+accessories+transmission)*conv)**2
    P2_a=P_a*K1*M_tot
    P2=P2_a+P2_cruise
    
    battery=R_bat/U_bat/U_bat*P2/conv/n_bat
    
    
    ### Final EC ###
    EC=rolling+drag+inertia+grade+wind+friction+copper+converter+accessories+transmission+battery

    ### Aggregated efficiencies ###
    engine_losses=friction+copper+converter+accessories
    transmission_losses=transmission
    battery_losses=battery
    nop_engine=ne*(1-engine_losses/(ntr*EC-transmission_losses))
    nop_transmission=ntr*(1-(transmission_losses)/EC)
    nop_battery=n_bat*(1-battery_losses/(ne*ntr*EC-transmission_losses-engine_losses))
    nop=nop_engine*nop_transmission*nop_battery

    
    return EC,[rolling,drag,inertia,grade,wind,friction,copper,converter,accessories,transmission,battery],[nop_engine,nop_transmission,nop_battery,nop]
    
    
    


# In[1]:


def PIEC_th (body,engine,trans,path,driver):
    
        ### inventories ###
    M_body,r0,Cd,A,Iw,Rw,transf,Pacc,M_eq,Cd_eq=body
    P_max,ne,D,fmep0,p0,Q0,N_idle,cs,stop_start=engine
    ntr,a_tr,S,Ne=trans
    J3p,K1p,K2p,rate_acc,J0p,H,w,urban,dist,t_idle=path
    B,mu_v,mu_a,mu_N,M_payload=driver
    LHV=fuel

    
    ### calculated parameters ###
    M_tot=M_body+M_payload+M_eq
    Cd=Cd*Cd_eq
    PaM=P_max/M_tot*mu_a
    sigma_t=transf/Rw
    conv=36
    
    ### computed parameters for integration model ###
    
    K1=K1p*mu_v*mu_v
    K2=K2p*mu_v*mu_v*mu_v
    ta=1/PaM*K1
    da=1/PaM*K2
    
    Nc=Ne*np.pi/30*mu_N
    N_idle=N_idle*np.pi/30
    Na=N_idle+np.sqrt(mu_a)*Na_max
    
    if Na<Nc:
        Na=Nc
    
    
    ### integration variables ###
    J1=1-K1/B
    J1_cruise=1-K1/B-da
    J0_cruise=J0p/mu_v*J1_cruise
    J3_cruise=mu_v*mu_v*J3p*J1_cruise
    J0=J0p/mu_v*(J1-da*(1-1/rate_acc))
    J3=mu_v*mu_v*J3p*(J1-da*(1-rate_acc*rate_acc))
    Chi1=urban*Nc*(J0_cruise)+(1-urban)*sigma_t*J1_cruise+Na*ta
    Chi3=urban*Nc*Nc*Nc*J0_cruise+(1-urban)*sigma_t*sigma_t*sigma_t*J3_cruise+Na*Na*Na*ta
    
    ### PIECs Calculations ###
    
    ### External forces computation ###
    
    rolling=r0*M_tot*g*J1/conv/ne/ntr
    drag=0.5*rho_air*Cd*A*J3/conv/ne/ntr
    inertia=(M_tot+4*Iw/Rw/Rw)*K1/conv/ne/ntr
    grade=M_tot*g*H/conv/ne/ntr
    wind=0.5*rho_air*Cd*A*w*w*J1/conv/ne/ntr
    
    ### powertrain losses computation ###
    
    friction=fmep0/(4*np.pi)*D*Chi1/conv/ne
    pumping=p0/(4*np.pi)*D*Chi3/conv/ne
    thermal=Q0*D*J0/conv/ne
    cold_engine=cs*P_max/conv/dist
    accessories=Pacc*(J0p+t_idle)/conv/ne
    transmission=a_tr*P_max*Chi1/conv/ntr/ne
    synchronization=urban*S/conv/ne
    idling=(fmep0/(4*np.pi)*D*N_idle*t_idle/conv/ne+p0/(4*np.pi)*D*N_idle*N_idle*N_idle*t_idle/conv/ne+Q0*D*t_idle/conv/ne)*stop_start
    
    
    MIEC = (r0*g*J1+K1+g*H)/conv/ne/ntr*100
    r0IEC= (M_tot*g*J1)/conv/ne/ntr/1000
    CdIEC=0.5*rho_air*Cd_eq*A*(J3+w*w*J1)/conv/ne/ntr/10
    AIEC=0.5*rho_air*Cd*(J3+w*w*J1)/conv/ne/ntr
    DIEC=(fmep0*(Chi1+N_idle*t_idle)+p0*(Chi3+N_idle*N_idle*N_idle*t_idle)+Q0*(J0+t_idle))/(4*np.pi)/conv/ne+cs*(P_max/D)/conv/dist+a_tr*(P_max/D)*Chi1/conv/ntr/ne
    SIEC=fmep0/(4*np.pi)*D*(1-urban)*J1_cruise/conv/ne+p0/(4*np.pi)*D*(1-urban)*3*sigma_t*sigma_t*J3_cruise/conv/ne+cs*(P_max/sigma_t)/conv/dist+a_tr*(P_max/sigma_t)*Chi1/conv/ntr/ne+a_tr*P_max*(1-urban)*J1_cruise/conv/ntr/ne
    f0IEC=D*Chi1/(4*np.pi)/conv/ne
    p0IEC=D*Chi3/(4*np.pi)/conv/ne/1000
    PaccIEC=(J0p+t_idle)/conv/ne*1000
    MIEC_SE=MIEC+(D/M_tot)*DIEC*100
    MIEC_SE_alt=MIEC+(sigma_t/M_tot)*SIEC*100
    
    return [MIEC,r0IEC,CdIEC,AIEC,DIEC,SIEC,f0IEC,p0IEC,PaccIEC,MIEC_SE,MIEC_SE_alt]


# In[ ]:

def PIEC_el (body,engine,trans,path,driver,battery):
    
    ### inventories ###
    M_body,r0,Cd,A,Iw,Rw,transf,Pacc,M_eq,Cd_eq=body
    P_e,Tmax,ne,alpha,epsilon,betha=engine
    a_tr,ntr=trans
    J3p,K1p,K2p,rate_acc,J0p,H,w,urban,dist,t_idle=path
    B,mu_v,mu_a,mu_N,M_payload=driver
    R_bat,U_bat,M_bat,n_bat=battery

    
    
    ### calculated parameters ###
    
    conv=36
    M_tot=M_body+M_payload+M_eq+M_bat
    PaM=P_e/M_tot*mu_a
    P_a=P_e*mu_a
    Cd=Cd*Cd_eq
    sigma_t=transf/Rw
    
    
    
    ## Regenerative Braking Efficiency ##
    if B>B_lim/2:
        nregen=1-(2*B-B_lim)*(2*B-B_lim)/(4*B*B)
    else:
        nregen=1

    
    ### computed parameters for integration model ###
    K1=K1p*mu_v*mu_v
    K2=K2p*mu_v*mu_v*mu_v
    ta=1/PaM*K1
    da=1/PaM*K2
    C2=(Tmax)*(mu_a*Tmax)*ta
    
    
    ### integration variables ###
    
    J1=1-K1/B*(1-rate_acc*rate_acc)
    J1a=J1-da*(1-rate_acc*rate_acc)
    J0=J0p/mu_v*(1-(K1/B-da)*(1-1/rate_acc))
    J3=mu_v*mu_v*J3p*(1-K1/B*(1-rate_acc*rate_acc)-da*(1-rate_acc*rate_acc))
    Chi1=sigma_t
    
    MIEC = (r0*g+K1*(1-nregen)+g*H)/conv/ne/ntr/n_bat*100
    r0IEC= (M_tot*g)/conv/ne/ntr/n_bat/1000
    CdIEC=0.5*rho_air*A*Cd_eq*(J3+w*w)/conv/ne/ntr/n_bat/10
    AIEC=0.5*rho_air*Cd*(J3+w*w)/conv/ne/ntr/n_bat
    PeIEC=a_tr*Chi1/conv/ntr/ne/n_bat*100000
    SIEC=alpha/conv/ne/n_bat+a_tr*P_e/conv/ntr/ne/n_bat
    PaccIEC=(J0p+t_idle)/conv/ne/n_bat*1000
    MIEC_SE=MIEC+(P_e/M_tot)*PeIEC*100
    MIEC_SE_alt=MIEC+(sigma_t/M_tot)*SIEC*100
    
    return [MIEC,r0IEC,CdIEC,AIEC,PeIEC,SIEC,PaccIEC,MIEC_SE,MIEC_SE_alt]


