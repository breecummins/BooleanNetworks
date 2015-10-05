#third party modules
import numpy as np
import matplotlib.pyplot as plt

t = np.arange(-2.0,2.0,0.01)
broad = lambda t: np.exp(-t**10)
pulse = lambda t: np.exp(-100*t**2)
fig = plt.figure()
plt.hold('on')
plt.plot(t,broad(t),'b-',linewidth=2.0)
plt.plot(t+0.25,broad(t),'r-',linewidth=2.0)
plt.plot(t+0.5,broad(t),'k-',linewidth=2.0)
plt.plot(t+0.75,broad(t),'g-',linewidth=2.0)
plt.plot(t+1.0,broad(t),'m-',linewidth=2.0)
plt.xlim(-1.25,2.25)
plt.ylim(-0.01,1.01)
plt.axis('off')
fig = plt.figure()
plt.hold('on')
plt.plot(t,pulse(t),'b-',linewidth=2.0)
plt.plot(t+0.25,pulse(t),'r-',linewidth=2.0)
plt.plot(t+0.5,pulse(t),'k-',linewidth=2.0)
plt.plot(t+0.75,pulse(t),'g-',linewidth=2.0)
plt.plot(t+1.0,pulse(t),'m-',linewidth=2.0)
plt.xlim(-1.25,2.25)
plt.ylim(-0.01,1.01)
plt.axis('off')
plt.show()


