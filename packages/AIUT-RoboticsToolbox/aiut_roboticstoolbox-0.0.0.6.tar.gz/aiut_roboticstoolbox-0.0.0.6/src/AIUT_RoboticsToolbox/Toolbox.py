#In the Name of Allah
# programmer : Maziar Palhang
# First Edit : Wed. 1399/12/6
# Last  Edit : Thu. 1402/2/3
# Last  Edit : Fri. 1402/2/8 class scara added, DH table is printed in a better way
#                            now changed to work with matplotlib7
# Last Edit  : Wed. 1403/12/8
# Last Edit  : Wed. 1403/12/21 now the default mode of degrees is radian, and we
#                              we can say whether we like to work with degree or not.
# Last Edit  : Thu. 1403/12/23 homogenous rotations and translation were added.

import math
from scipy.linalg import logm, expm, inv
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.ticker as ticker

def version():
    print('AIUT_RoboticsToolbox 0.0.0.0.6, Esfand 1403')
    return

def rotx(ang, mode='rad'):
    if mode == 'deg':
        ang = math.radians(ang)
    r = np.array([[1.0, 0.0,    0.0],
         [0.0, math.cos(ang), -math.sin(ang)],
         [0.0, math.sin(ang), math.cos(ang)]])        
    return r

def roty(ang, mode='rad'):
    if mode == 'deg':
        ang = math.radians(ang)
    r = np.array([[math.cos(ang), 0.0, math.sin(ang)],
         [0.0,         1.0, 0.0],
         [-math.sin(ang),0.0, math.cos(ang)]])         
    return r

def rotz(ang, mode='rad'):
    if mode == 'deg':
        ang = math.radians(ang)
    r = np.array([[math.cos(ang), -math.sin(ang), 0.0],
         [math.sin(ang), math.cos(ang),  0.0],
         [0.0,         0.0,          1.0]])
         
    return r    

def hrotx(ang, mode='rad'):
    if mode == 'deg':
        ang = math.radians(ang)
    r = np.array([[1.0, 0.0,    0.0, 0.0],
         [0.0, math.cos(ang), -math.sin(ang), 0.0],
         [0.0, math.sin(ang), math.cos(ang) , 0.0],
         [0.0,           0.0,          0.0,   1.0]])        
    return r

def hroty(ang, mode='rad'):
    if mode == 'deg':
        ang = math.radians(ang)
    r = np.array([[math.cos(ang), 0.0, math.sin(ang), 0.0],
                  [0.0,           1.0,           0.0, 0.0],
                  [-math.sin(ang),0.0, math.cos(ang), 0.0],
                  [0.0           ,0.0,           0.0, 1.0]])         
    return r

def hrotz(ang, mode='rad'):
    if mode == 'deg':
        ang = math.radians(ang)
    r = np.array([[math.cos(ang), -math.sin(ang), 0.0, 0.0],
                  [math.sin(ang), math.cos(ang),  0.0, 0.0],
                  [0.0,           0.0,            1.0, 0.0],
                  [0.0,           0.0,            0.0, 1.0]])
         
    return r    

def htransl(x,y,z):
    t = [[1,0,0,x],
         [0,1,0,y],
         [0,0,1,z],
         [0,0,0,1]]
    return t

def rpy2r(gamma,beta,alpha,mode='rad'):
    if mode == 'deg':
        r = rotz(alpha,'deg').dot(roty(beta,'deg').dot(rotx(gamma,'deg')))
    else:
        r = rotz(alpha).dot(roty(beta).dot(rotx(gamma)))
    return r

def r2rpy(r,mode='rad'):
    beta = math.atan2(-r[2][0], math.sqrt(r[0][0]**2 + r[1][0]**2))
    if (math.cos(beta) != 0.0):
        alpha = math.atan2(r[1][0]/math.cos(beta), r[0][0]/math.cos(beta))
        gamma = math.atan2(r[2][1]/math.cos(beta), r[2][2]/math.cos(beta))
    elif beta == math.pi/2:
        alpha = 0.0
        gamma = math.atan2(r[0][1],r[1][1])
    else:
        alpha = 0.0
        gamma = -math.atan2(r[0][1],r[1][1])
    if mode == 'deg':             
        gamma = gamma*180/math.pi
        alpha = alpha*180/math.pi
        beta =  beta*180/math.pi
    return [gamma, beta, alpha]

def euler2r(alpha,beta,gamma, mode='rad'):
    if mode == 'deg':
        r = rotz(alpha,'deg').dot(roty(beta,'deg').dot(rotz(gamma,'deg')))
    else:
        r = rotz(alpha).dot(roty(beta).dot(rotz(gamma)))
    return r

def r2euler(r, mode='rad'):
    beta = math.atan2(math.sqrt(r[2][0]**2 + r[2][1]**2),r[2][2])
    if (math.sin(beta) != 0.0):
        alpha = math.atan2(r[1][2]/math.sin(beta), r[0][2]/math.sin(beta))
        gamma = math.atan2(r[2][1]/math.sin(beta), r[2][0]/math.sin(beta))
    elif beta == 0.0:
        alpha = 0.0
        gamma = math.atan2(-r[0][1],r[0][0])
    else:
        alpha = 0.0
        gamma = math.atan2(r[0][1],-r[0][0])

    if mode == 'deg':
        gamma = gamma*180/math.pi
        alpha = alpha*180/math.pi
        beta =  beta*180/math.pi
    return [gamma, beta, alpha]

# added 1400/12/12
def angvec2r(theta,v,mode='rad'):
    if mode == 'deg':
        a = math.radians(theta)
    else:
        a = theta
    st = math.sin(a)
    ct = math.cos(a)
    vt = 1 - ct
    r = np.array(
        [[v[0]*v[0]*vt+ct,      v[0]*v[1]*vt-v[2]*st, v[0]*v[2]*vt+v[1]*st],
         [v[0]*v[1]*vt+v[2]*st, v[1]*v[1]*vt+ct,      v[1]*v[2]*vt-v[0]*st],
         [v[0]*v[2]*vt-v[1]*st, v[1]*v[2]*vt+v[0]*st, v[2]*v[2]*vt+ct],])
    
    return r

# added 1400/12/12
def r2angvec(r,mode='rad'):
    a = (r[0][0]+r[1][1]+r[2][2]-1)/2.0
    ang = math.acos(a)
    if np.isclose(ang,0):
        return [0, [1,0,0]]  # not rotation
    theta = math.acos(a)
    if mode == 'deg':
        theta = math.degrees(theta)
    v = [r[2][1]-r[1][2], r[0][2]-r[2][0], r[1][0]-r[0][1]]
    v = np.multiply(v,0.5/math.sin(ang))
    
    return [theta,v]

# added 1400/12/12
def r2angvec2(r,mode='rad'):
    a = (np.trace(r)-1)/2.0
    ang = math.acos(a)
    if np.isclose(ang,0):
        return [0, [1,0,0]]  # not rotation
    theta = math.acos(a)
    if mode == 'deg':
        theta = math.degrees(theta)
    v = [r[2][1]-r[1][2], r[0][2]-r[2][0], r[1][0]-r[0][1]]
    v = np.multiply(v,0.5/math.sin(ang))
    
    return [theta,v]

#make a skew matrix from a vector
# added 1400/12/12
def vec2skew(k):
    r = np.array([[0,    -k[2], k[1]],
                  [k[2],  0,   -k[0]],
                  [-k[1], k[0], 0]])
    return r

# finds the vector corresponding to a skew matrix
# added Tue. 1403/12/21
def skew2vec(S):
    v = np.array([S[2][1],S[0][2],S[1][0]])
    return v

def vec2skewa(k):
    r = np.array([[0,    -k[5], k[4], k[0]],
                  [k[5],  0,   -k[3], k[1]],
                  [-k[4], k[3], 0   , k[2]],
                  [0,     0,    0   , 0]])
    return r

def skewa2vec(S):
    v = np.array([S[0][3],S[1][3],S[2,3],S[2][1],S[0][2],S[1][0]])
    return v

#finds the skew matrix corresponding to a rotation matrix
def r2Caleyskew(r):
    I = np.eye(3)
    IPlusRInv = inv(I+r)
    S = (I-r)@IPlusRInv
    return S

# finds the corresponding rotation matrix from Caley skew matrix
def Caleyskew2r(S):
    I = np.eye(3)
    r = inv(I-S)
    r = r@(I+S)
    return r

# finds the matrix logarithm of a rotation matrix
# it accually finds the skew matrix of the rotation matrix.
def mlog(r):
    return logm(r)

# finds the matrix exponentition of a matrix.
# It ectually finds the corresponding rotation matrix of
# tht skew matrix.
def mexp(S):
    return expm(S)

# drawing a rotation matrix
# added 1400/12/12
def plot(r):
    fig = plt.figure(1)
    ax = fig.add_subplot(projection='3d')
    ax.plot3D([0,r[0][0]],
              [0,r[1][0]],
              [0,r[2][0]],'r')
    ax.plot3D([0,r[0][1]],
              [0,r[1][1]],
              [0,r[2][1]],'g')
    ax.plot3D([0,r[0][2]],
              [0,r[1][2]],
              [0,r[2][2]],'b')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()
    return

# draw a homogeneous transformation matrix
# added Mon. 1403/12/20
def hplot(TT):
    fig = plt.figure(1)
    ax = fig.add_subplot(projection='3d')
    ax.plot3D([TT[0][3],TT[0][3]+TT[0][0]],
              [TT[1][3],TT[1][3]+TT[1][0]],
              [TT[2][3],TT[2][3]+TT[2][0]],'r')
    ax.plot3D([TT[0][3],TT[0][3]+TT[0][1]],
              [TT[1][3],TT[1][3]+TT[1][1]],
              [TT[2][3],TT[2][3]+TT[2][1]],'g')
    ax.plot3D([TT[0][3],TT[0][3]+TT[0][2]],
              [TT[1][3],TT[1][3]+TT[1][2]],
              [TT[2][3],TT[2][3]+TT[2][2]],'b')
    minAll = min(TT[0][3],TT[1][3],TT[2][3])
    maxAll = max(TT[0][3],TT[1][3],TT[2][3])
    ax.set_xlim(minAll-1, maxAll+1)
    ax.set_ylim(minAll-1, maxAll+1)
    ax.set_zlim(minAll-1, maxAll+1)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()
    return

class SerialLink:

    def __init__(self, name, links):
        self.name  = name
        self.links = links
        print(self.name)
        print('--------------------------------------------')
        print('i\talpha\ta\td\ttheta\ttype')
        print('--------------------------------------------')
        for i in range(np.size(self.links,0)):
            print(i+1, end='\t')
            for j in range(np.size(self.links,1)):
                print(round(self.links[i][j],2), end='\t')
            print('\n')
        print('------------------------------------------')
        
    #Friday 1402/2/8
    def toDeg(self,radVal):
        return radVal*180.0/np.pi

    #create T i w.r.t i-1
    def makeT(self,DH):
        T = np.array([[math.cos(DH[3]),                -math.sin(DH[3]),  0,  DH[1]],
                     [math.sin(DH[3])*math.cos(DH[0]), math.cos(DH[3])*math.cos(DH[0]), -math.sin(DH[0]), -DH[2]*math.sin(DH[0])],
                     [math.sin(DH[3])*math.sin(DH[0]), math.cos(DH[3])*math.sin(DH[0]),  math.cos(DH[0]),  DH[2]*math.cos(DH[0])],
                     [0,                                0,                                0,                1]])
        return T

    def fkinCalc(self):
        TT = np.eye(4)
        for l in range(np.size(self.links,0)):
            T = self.makeT(self.links[l])
            TT = TT.dot(T)
            
        return TT
    
    def fkin(self,joints):
        noOfJoints = np.size(joints)
        if noOfJoints != np.size(self.links,0):
            print('Number of specified joints is not correct.')
            return
        
        for i in range(np.size(joints)):
            if self.links[i][4] == 0:
                self.links[i][3] = joints[i]
            else:
                self.links[i][2] = joints[i]
        
        T = self.fkinCalc()
        return T
    
    def plot(self):
        fig = plt.figure(1)
        ax = fig.add_subplot(projection='3d')
        TT = np.eye(4)
        for i in range(np.size(self.links,0)):
            To = TT
            TT = TT.dot(self.makeT(self.links[i]))
            ax.plot3D([To[0][3],TT[0][3]],[To[1][3],TT[1][3]],[To[2][3],TT[2][3]])
        ax.plot3D([TT[0][3],TT[0][3]+2*TT[0][0]],
                  [TT[1][3],TT[1][3]+2*TT[1][0]],
                  [TT[2][3],TT[2][3]+2*TT[2][0]],'r')
        ax.plot3D([TT[0][3],TT[0][3]+2*TT[0][1]],
                  [TT[1][3],TT[1][3]+2*TT[1][1]],
                  [TT[2][3],TT[2][3]+2*TT[2][1]],'g')
        ax.plot3D([TT[0][3],TT[0][3]+2*TT[0][2]],
                  [TT[1][3],TT[1][3]+2*TT[1][2]],
                  [TT[2][3],TT[2][3]+2*TT[2][2]],'b')

        minAll = min(TT[0][3],TT[1][3],TT[2][3])
        maxAll = max(TT[0][3],TT[1][3],TT[2][3])
        ax.plot3D([0, 0],[0,0],[0,minAll-1],'y')
        ax.set_xlim(minAll-1, maxAll+1)
        ax.set_ylim(minAll-1, maxAll+1)
        ax.set_zlim(minAll-1, maxAll+1)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        plt.show()
        return 

    
class Puma560(SerialLink):
    def __init__(self,name):
        self.name = name
        a2 = 43.2
        a3 = 0    #10
        d3 = 0    #23.3
        d4 = 43.2
        self.links = [[0.0,     0.0,   0.0,  0.0, 0],
                      [-np.pi/2,0.0,   0.0,  0.0, 0],
                      [0.0,     a2,    d3,   0.0, 0],
                      [-np.pi/2,a3,    d4,   0.0, 0],
                      [np.pi/2, 0.0,   0.0,  0.0, 0],
                      [-np.pi/2,0.0,   0.0,  0.0, 0]]
        SerialLink.__init__(self,self.name,self.links)

#scara robot Friday 1402/2/8
class SCARA(SerialLink):
    def __init__(self,name,l1,l2):
        self.name = name
        self.l1 = l1
        self.l2 = l2
        self.links = [[0.0,     0.0,   0.0,  0.0, 0],
                      [0.0,     l1,    0.0,  0.0, 0],
                      [0.0,     l2,    0.0,  0.0, 0],
                      [np.pi,   0.0,   0.0,  0.0, 1]]
        SerialLink.__init__(self,self.name,self.links)


    def invKin(self,T,type='r'):
        results = []
        theta123 = math.atan2(T[1][0],T[0][0])
        d4 = -T[2][3]
        x = T[0][3]
        y = T[1][3]
        c2 = (x*x+y*y-self.l1*self.l1-self.l2*self.l2)/(2*self.l1*self.l2)
        if (c2 < -1 or c2 > 1):
            print('invalid location')
            return []     
        s2 = math.sqrt(1-c2*c2)
        theta2 = math.atan2(s2,c2)
        k1 = self.l1 + self.l2*c2
        k2 = self.l2*s2
        theta1 = math.atan2(y,x) - math.atan2(k2,k1)
        theta3 = theta123 - theta1 - theta2
        if type == 'r':   #use radians
            joints = [theta1,theta2,theta3,d4]
        elif type == 'd': #use degrees
            joints = [self.toDeg(theta1),self.toDeg(theta2),self.toDeg(theta3),d4]            
        results.append(joints)
        
        s2 = -s2
        theta2 = math.atan2(s2,c2)
        k1 = self.l1 + self.l2*c2
        k2 = self.l2*s2
        theta1 = math.atan2(y,x) - math.atan2(k2,k1)
        theta3 = theta123 - theta1 - theta2
        if type == 'r':  #use radians
            joints = [theta1,theta2,theta3,d4]
        elif type == 'd': #use degrees
            joints = [self.toDeg(theta1),self.toDeg(theta2),self.toDeg(theta3),d4]
        results.append(joints)
        
        return results
