import numpy as np

class move:
    def __init__(self,x,y,v):
        self.v=v
        self.x=x
        self.y=y

    def accelerate(self,l1,l2,deg,a,time):
        self.v +=a*0.01
        d = self.v*0.01 + (a*0.01**2)/2
        self.x += d*np.cos(np.radians(deg))
        self.y += d*np.sin(np.radians(deg))
        s1 = np.degrees(np.arctan(self.y/self.x)) - np.degrees(np.arccos((l1**2+self.x**2+self.y**2-l2**2)/(2*l1*np.sqrt(self.x**2+self.y**2))))
        s2 = np.degrees(np.pi - np.arccos((l1**2+l2**2-self.x**2-self.y**2)/(2*l1*l2)))
        return s1,s2

    def steady(self,l1,l2,deg,time):
        d = self.v*0.01
        self.x += d*np.cos(np.radians(deg))
        self.y += d*np.sin(np.radians(deg))
        s1 = np.degrees(np.arctan(self.y/self.x)) - np.degrees(np.arccos((l1**2+self.x**2+self.y**2-l2**2)/(2*l1*np.sqrt(self.x**2+self.y**2))))
        s2 = np.degrees(np.pi - np.arccos((l1**2+l2**2-self.x**2-self.y**2)/(2*l1*l2)))
        return s1,s2

    def decelerate(self,l1,l2,deg,a,time):
        self.v -= a*0.01
        d = self.v*0.01 - (a*0.01**2)/2
        self.x += d*np.cos(np.radians(deg))
        self.y += d*np.sin(np.radians(deg))
        s1 = np.degrees(np.arctan(self.y/self.x)) - np.degrees(np.arccos((l1**2+self.x**2+self.y**2-l2**2)/(2*l1*np.sqrt(self.x**2+self.y**2))))
        s2 = np.degrees(np.pi - np.arccos((l1**2+l2**2-self.x**2-self.y**2)/(2*l1*l2)))
        return s1,s2
    

class calculate:
    def tip(self,l1,l2,s1,s2):
        tip_x = l1*np.cos(np.radians(s1))+l2*np.cos(np.radians(s1+s2))
        tip_y = l1*np.sin(np.radians(s1))+l2*np.sin(np.radians(s1+s2))
        return tip_x,tip_y

    def ang_v(self,s1,s2):
        #solidworksでは[deg/sec]なので合わせた
        return s1/0.01,s2/0.01

    def torque(self,l1,l2,m1,m2,s1,s2):
        a1 = np.radians(s1)/0.01**2     #普通角速度、角加速度は[rad/sec]
        a2 = np.radians(s2)/0.01**2
        omega = np.array([a1, a2])
        I1 = (4*m1*(l1/2)**2)/3 
        I2 = (4*m2*(l2/2)**2)/3 
        M1 = m1*(l1/2)**2+m2*l1**2+m2*l2/2+I1+I2+2*m2*l1*(l2/2)*np.cos(np.radians(s2))
        M2 = m2*(l2/2)**2+I2+m2*l1*(l2/2)*np.cos(np.radians(s2))
        M3 = m2*(l2/2)**2+I2+m2*l1*(l2/2)*np.cos(np.radians(s2))
        M4 = m2*(l2/2)**2+I2
        M = np.array([[M1, M2], [M3, M4]])
        V1 = -m2*l1*(l2/2)*(2*(np.radians(s1)/0.01)*(np.radians(s2)/0.01)+(np.radians(s2)/0.01)**2)*np.sin(np.radians(s2))
        V2 = -m2*l1*(l2/2)*(np.radians(s1)/0.01)**2*np.sin(np.radians(s2))
        V = np.array([V1, V2])
        T = np.dot(M,omega)+V
        return T[0],T[1]



