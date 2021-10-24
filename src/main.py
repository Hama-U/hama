import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from classes import move,calculate

'''擬似シュミレーター'''

#define
l1, l2 = 300,300        #リンク長[mm]
m1,m2 = 20,20           #各リンクの重さ[kg]
sec = 1                 #直線運動にかかる時間[sec]
acc_t = 0.2             #加速(減速)にかける時間[sec]
x,y,deg=[400,100,400],[100,80,50],[180,0]   #(x,y)=(400,100)⇄(100,100)
#x,y,deg=[150,150,150],[150,-150,150],[270,90]   #(x,y)=(150,150)⇄(150,-150)

#create dataset
dataset = {"time":[],"theta 1":[],"theta 2":[],"x":[],"y":[],"v":[],"ang_v1":[],"ang_v2":[],"τ1":[],"τ2":[]}
key = list(dataset.keys())

#simulation
time,index = 0,0
ins01 = move(x[0],y[0],0)
ins02 = calculate()
for i in range(len(x)-1):
    if (l1+l2)<np.sqrt(x[i]**2+y[i]**2):
        print("リンクの長さが足りていません")
        sys.exit()
    t=0
    a = (np.sqrt((x[i+1]-x[i])**2+(y[i+1]-y[i])**2)/(sec-acc_t))/acc_t
    while t<acc_t: #accelerate
        time=round(time,3)
        theta = ins01.accelerate(l1,l2,deg[i],a,time)
        tip = ins02.tip(l1,l2,theta[0],theta[1])
        if time==0:
            d_s1 = 0
            d_s2 = 0
        else:
            d_s1 = theta[0]-dataset['theta 1'][index-1]
            d_s2 = theta[1]-dataset['theta 2'][index-1]
        angv = ins02.ang_v(d_s1,d_s2)
        tau = ins02.torque(l1/1000,l2/1000,m1,m2,d_s1,d_s2)
        tmp = [time,theta[0],theta[1],tip[0],tip[1],ins01.v,angv[0],angv[1],tau[0],tau[1]]
        for j in range(len(key)):
            dataset[key[j]].append(tmp[j])
        t+=0.01
        time+=0.01
        index+=1
    while t<sec-acc_t:   #steady
        time=round(time,3)
        theta = ins01.steady(l1,l2,deg[i],time)
        tip = ins02.tip(l1,l2,theta[0],theta[1])
        d_s1 = theta[0]-dataset['theta 1'][index-1]
        d_s2 = theta[1]-dataset['theta 2'][index-1]
        angv = ins02.ang_v(d_s1,d_s2)
        tau = ins02.torque(l1/1000,l2/1000,m1,m2,d_s1,d_s2)
        tmp = [time,theta[0],theta[1],tip[0],tip[1],ins01.v,angv[0],angv[1],tau[0],tau[1]]
        for j in range(len(key)):
            dataset[key[j]].append(tmp[j])
        t+=0.01
        time+=0.01
        index+=1
    while t<sec:     #decelerate
        time=round(time,3)
        theta = ins01.decelerate(l1,l2,deg[i],a,time)
        tip = ins02.tip(l1,l2,theta[0],theta[1])
        d_s1 = theta[0]-dataset['theta 1'][index-1]
        d_s2 = theta[1]-dataset['theta 2'][index-1]
        angv = ins02.ang_v(d_s1,d_s2)
        tau = ins02.torque(l1/1000,l2/1000,m1,m2,d_s1,d_s2)
        tmp = [time,theta[0],theta[1],tip[0],tip[1],ins01.v,angv[0],angv[1],tau[0],tau[1]]
        for j in range(len(key)):
            dataset[key[j]].append(tmp[j])
        t+=0.01
        time+=0.01
        index+=1
    

#dataframe
data = pd.DataFrame(dataset)
pd.DataFrame.to_csv(data,path_or_buf="data/data.csv",index=False)
pd.DataFrame.to_csv(data,path_or_buf="data/theta1.csv",header=False,index=False,columns=["time","theta 1"])
pd.DataFrame.to_csv(data,path_or_buf="data/theta2.csv",header=False,index=False,columns=["time","theta 2"])


#plot graph
fig = plt.figure(figsize=(12, 6))
fig.suptitle("Demo Simulater\n(l1=%d,l2=%d)"%(l1,l2), size=16, weight=2, color="black")
ax1 = fig.add_subplot(231)
ax2 = fig.add_subplot(232)
ax3 = fig.add_subplot(233)
ax4 = fig.add_subplot(234)
ax5 = fig.add_subplot(235)
ax6 = fig.add_subplot(236)
ax1.plot(data["time"], data["theta 1"], label="θ1")
ax2.plot(data["time"], data["theta 2"], label="θ2")
ax3.plot(data["time"], data["v"], label="v")
ax4.plot(data["time"], data["x"], label="x",color='blue')
ax4.plot(data["time"], data["y"], label="y",color='red')
ax5.plot(data["time"], data["ang_v1"], label="ω1",color='blue')
ax5.plot(data["time"], data["ang_v2"], label="ω2",color='red')
ax6.plot(data["time"], data["τ1"], label="τ1",color='blue')
ax6.plot(data["time"], data["τ2"], label="τ2",color='red')
ax1.legend()
ax2.legend()
ax3.legend()
ax4.legend()
ax5.legend()
ax6.legend()
plt.tight_layout()
plt.show()
