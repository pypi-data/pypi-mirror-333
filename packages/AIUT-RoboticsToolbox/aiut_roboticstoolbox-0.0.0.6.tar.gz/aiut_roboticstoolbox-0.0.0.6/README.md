# A Robotics Toolbox from Maziar Palhang

This is a simple Robotics Toolbox package.

To install this package:\
on windows:\
py -m pip install AIUT_RoboticsToolbox\
\
on Linux and Mac:\
python3 -m pip install AIUT_RoboticsToolbox\
\
To upgrade:\
on Windows:\
py -m pip install AIUT_RoboticsToolbox --upgrade\
\
on Linux and Mac:\
python3 -m pip install AIUT_RoboticsToolbox --upgrade\
To use this package in your program, add the following line:\
from AIUT_RoboticsToolbox.Toolbox import *

## Routines:
version()             #prints the version of the toolbox
rotx(ang, mode='rad') # mode='rad' or 'deg', default is 'rad'\
roty(ang, mode='rad') # mode='rad' or 'deg', default is 'rad'\
rotz(ang, mode='rad') # mode='rad' or 'deg', default is 'rad'\
\
hrotx(ang, mode='rad') # homogeneous rotation about x, mode='rad' or 'deg', default is 'rad'\
hroty(ang, mode='rad') # homogeneous rotation about y, mode='rad' or 'deg', default is 'rad'\
hrotz(ang, mode='rad') # homogeneous rotation about z, mode='rad' or 'deg', default is 'rad'\
htransl(x,y,z)         # homogeneous translation \
\
rpy2r(gamma,beta,alpha, mode='rad')  # XYZ rotation\
r2rpy(r, mode='rad')\
euler2r(alpha,beta,gamma, mode='rad') # ZYZ rotation\
r2euler(r, mode='rad')\
angvec2r(theta,v, mode='rad')\
r2angvec(r, mode='rad')\
\
vec2skew(k)         #make a skew matrix from a 3 element vector\
skew2vec(S)         #make a 3 element vector from a skew matrix \
vec2skewa(k)        #make an augmented skew matrix from a 6 element vector\
skewa2vec(S)        #make a 6 element vector from an augmented skew matrix \
r2skew(r)           #finds the corresponding skew matrix of a rotation matrix \
\
mlog(r)             #finds the matrix logarithm of r \
mexp(S)             #finds matrix exponentiation of skew matrix S\
\
plot(r)             #plot a rotation matrix\
hplot(T)            #plot a frame \

## Classes:

SerialLink(name,links)\
Puma560(name)\
SCARA(name,l1,l2)\
