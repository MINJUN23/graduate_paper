import matplotlib.pyplot as plt
import numpy as np
from math import log10

v = np.arange(-3.0, 3.0, 0.01)
J = -6.9-20*np.log10(np.sqrt(np.square(v-0.1)+1)+v-0.1)
line, = plt.plot(v, J, lw=2)


plt.show()