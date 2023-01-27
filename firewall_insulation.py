# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

Working around CS.23 regualations for mininum distance between electronics and firewall

"""

import numpy as np

T_w_1 = 1373 #K CS23 regulations - firewall temperature
T_w_2 = 293 #K ambient temperature to start 
L = 0.105 #m distance between electronics and firewall 
H = 0.220 #m height of walls aka pdu+junction box height
W = 0.7 #estimate - check later in cad model
e_1 = 0.09 #emmitance of aluminium 
e_2 = 0.07 #emmitance of stainless steel (firewall) need to check - also goes up with temp
F12 = 1/((1/e_1)+(1/e_2)-1)
stef_bolt = 5.67*(10**-8) 

#Table A.7 heat transfer book 800K
k_air_800K = 0.0559 #W/mK
rho_air_800K = 0.442 #kg/m^3
v_air_800K = 81.20*(10**-6) #m^2/s
Pr_air_800K = 0.7
beta_air_800K = 0.4*(10**-3) #K^-1 (researched online)
g = 9.81 #m/s^2


#for a range 10^3 < RaL < 10^7 equations nusselt number are valid - yes valid for this case
RaL = (beta_air_800K*(T_w_1-T_w_2)*g*(L**3)*Pr_air_800K)/(v_air_800K**2)

#nusselt number equations from page 303 heat transfer book
Nu_1 = 0.0605*(RaL**(1/3))
Nu_2 = (1+((0.104*(RaL**0.293))/(1+(6310/RaL)**1.36))**3)**1/3
Nu_3 = 0.242*((RaL/(H/L))**0.272)
NuL_90deg = max(Nu_1,Nu_2,Nu_3)

h_c = (k_air_800K/L)*NuL_90deg

q_conv = h_c*(T_w_1-T_w_2)
q_rad = F12*stef_bolt*((T_w_1**4)-(T_w_2**4))

q_tot = q_conv + q_rad

Q_total_dot = q_tot*H*W #area

#heat absorbed by electronics
m = 0.2 #kg insulation wire eg pvc
T_pvc_melt = 533 #K insulation melting point
T_amb = 293 #K
c = 840 #J/kgK specific heat pvc

Q = m*c*(T_pvc_melt-T_amb)

#time to heat to melting point
delta_t = (Q/Q_total_dot)/60

#wrong assumptions - temp changes through time, air constants change through time 
#thus the heat transfer changes through time; not constant


#solution 1 - radiation block sheet
e_1_update = 0.02
F12_update = 1/((1/e_1_update)+(1/e_2)-1)
q_rad_update = F12_update*stef_bolt*((T_w_1**4)-(T_w_2**4))

diff_rad = 100*((q_rad - q_rad_update)/q_rad)

#solution 2 - fibreglass insulation
k = 0.048 #W/mK
x = 0.05 #m 
e_2_update = 0.75
F12 = 1/((1/e_1_update)+(1/e_2_update)-1)

T_w_1_0 = 1373
T_w_2_0 = 293
T_air_0 = 293
t = np.linspace(0,900,1000)

T_w_1 = [T_w_1_0]
T_w_2 = [T_w_2_0]
T_air = [T_air_0]

q_cond = [(k/x)*(T_w_1_0-T_w_2_0)]
#q_rad = [F12*stef_bolt*((T_w_2_0**4)-(T_air_0**4))]
q_conv = [h_c*(T_w_2_0-T_air_0)]
q_net = [(k/x)*(T_w_1_0-T_w_2_0) - h_c*(T_w_2_0-T_air_0)] #F12*stef_bolt*((T_w_2_0**4)-(T_air_0**4)) - 
m_fib = 7 #kg
c_fib = 700 #J/kgK
m_air = H*W*x*1.225 #kg
c_air = 700 #J/kgK


for i in range(len(t)): 
        T_w_2.append(T_w_1[-1]-q_net[-1]/m_fib*c_fib)
        T_air.append(T_air[-1]+q_conv[-1]/m_air*c_air)
        q_cond.append((k/x)*(T_w_1[-1]-T_w_2[-1]))
        #q_rad.append(F12*stef_bolt*((T_w_2[-1]**4)-(293**4)))
        q_conv.append(h_c*(T_w_2[-1]-T_air[-1]))
        q_net.append(q_cond[-1] -  q_conv[-1]) # - q_rad[-1])


