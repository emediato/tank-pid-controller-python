from GVL import *
from mainpythreads import *
import threading
import numpy as np
from threading import Condition, Lock
from simple_pid import PID
from threading import Thread
import os
import math
import time

#import collections
#actuatorcollection1 = deque()
#actuatorcollection2 = deque()
#hlcollectioin1 = deque()
#hlcollectioin2 = deque()
# Control
#i=0

def softPLCthread():
    global actuatort1, actuatort2, levelh1, levelh2, outq1, outq2;
    kp = 1
    ki = 0.025
    kd = 0.0125
    pidt1 = PID(kp, ki, kd, setpoint=levelh1)
    pidt2 = PID(kp, ki, kd, setpoint=levelh2)

    while (dydx(outq1, levelh1) == False or (dydx(outq2, levelh2)) == False ):
        #legends1[i] = actuatort1
        #legends2[i] = actuatort2
        #i = i + 1
        #actuatorcollection1.append (actuatort1)
        #actuatorcollection2.append (actuatort2)

        legends1.append(actuatort1)
        legends2.append(actuatort2)

        #print (actuatort1)

        if (dydx(outq1, levelh1) == False ):
            condition.acquire()
            try:
                actuatort1 = pidt1(outq1)
            finally:
                condition.release()

        if (dydx(outq2, levelh2)== False ):
            # and (outq1>0.5)):
            condition.acquire()
            try:
                actuatort2 = pidt2(outq2)
            finally:
                condition.release()
        event.wait(0.2)

# Tank 1
# Q = VA :. vazao = velocidade x area
#j=0

# Using Runge Kutta Method of order 4 to approximate y(1) if the following IVP:
# (dy/dt) = realvalue - 0.1y(t), 0 <= t <= 1
# y(0) = 0

def tankthread1(height, Q, lowr1, upperR1):
    #print("t1")
    global actuatort1, actuatort2, levelh1, levelh2, outq1, outq2, legendsh1, legendsh2;
    while ( (dydx(outq2, levelh2)) == False or (dydx(outq1, levelh1)) == False ):
        legendsh1.append(outq1)
        legendsh2.append(outq2)
        #hlcollectioin1.append(outq1)
        #hlcollectioin2.append(outq2)
        num = actuatort1 - (Q * math.sqrt(outq1)) - actuatort2
        div = math.pi * pow((lowr1 + ((upperR1 - lowr1) / height) * outq1), 2)
        #div = math.pi * ((lowr1 + ((upperR1 - lowr1)) / height * outq1 ) ** 2)
        #div = max(0, div)
        dynamic =  num / div
        condition.acquire()
        try:
            condition.notify()
            outq1 = outq1 + (dynamic*0.1) ##f tank
        finally:
            condition.release()
        event.wait(0.1)

    #    threading.Timer(0.1, processthread1).start()

# Tank 2
def tankthread2(height, Q, lowr2, upperR2):
        #print("t2")
        global actuatort1, actuatort2, levelh1, levelh2, outq1, outq2;

        while ( dydx(outq2, levelh2)== False   ):
            num = actuatort2 - (Q * math.sqrt(outq2))
            div =  math.pi * pow((lowr2 + ((upperR2 - lowr2) / height) * outq2), 2)
            #math.pi * ((lowr2 + ((upperR2 - lowr2)) / height) * outq2) ** 2
            #div = max(0, div)
            dynamic = num / div

            condition.acquire()
            condition.notify()

            outq2 = outq2 + (dynamic * 0.1)
            condition.release()
            event.wait(0.1)
                #if ( (dydx(outq2, levelh2)) == True ):
                #    print(process_thread_2.getName(), " Full!")
                #    break
# comparing absolute sample differential inequation "dy/dx < |(x - y)|"
def dydx(x, y):
#    print("\nRelative accuracy: abs((yApprox - yExact)/yExact)")
    dif = 0.00001
    if abs(x - y) < dif:
        return True
    else:
        return False
