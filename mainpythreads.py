
# -------------- thread control block
# parent process pointer
# thread id TID
# thread state
# program counter
# register set
# stack pointer

# -------------- processs memory
#stack
#data
#text
import math
import numpy as np
import threading
import os
import time
import sched
import logging
from simple_pid import PID
from datetime import datetime
from threading import Thread
# global variables list
from threading import Condition, Lock
from threading import Thread
from GVL import *
from defthreads import *
import matplotlib.pyplot as plt

lock = threading.RLock()
condition = Condition(lock)
event = threading.Event()


if __name__ == "__main__":
    start = time.time()
    # creating threads
    #main()
    t1 = threading.Thread(target=tankthread1, name='T1' , args=( 3, 0.4, 0.9, 1) )
    t2 = threading.Thread(target=tankthread2, name='T2' , args=( 2, 0.3, 0.9, 0.5) )
    controlt = threading.Thread(target=softPLCthread, name='softplc')

    t1.start()
    t2.start()
    controlt.start()
    # wait until all threads finish
    t1.join()
    t2.join()
    controlt.join()
    end = time.time()

    print ("Time elapsed: %.2f secs" % ( end - start))
    g1 = np.arange(0.0, len(legends1), 1)
    g2 = np.arange(0.0, len(legends2), 1)
    g3 = np.arange(0.0, len(legendsh1), 1)
    g4 = np.arange(0.0, len(legendsh2), 1)
#actuatorss
    plt.figure()
    plt.subplot(211)
    plt.plot(g1, legends1, 'r--')
    plt.plot(g2, legends2, 'k')

#levels
    plt.subplot(212)
    plt.plot(g3, legendsh1, 'r--')
    plt.plot(g4, legendsh2, 'k')
    plt.show()

    #periodo 0,2  = frequencia 5/s para simular EDO
    #frequencias menores executadas antes
