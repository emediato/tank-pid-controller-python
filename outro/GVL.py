from tppronto import *
from var import *

import threading
import random, time
import numpy as np
from threading import Condition, Lock
from simple_pid import PID
from threading import Thread
import os
import math
def aprox_equal(x,y):
    tolerancia= 0.00001
    if abs(x-y) < tolerancia:
        return True
    else:
        return False

def control():
    global atuador_t1,set_point_t1,real_t1_altura,atuador_t2,set_point_t2,real_t2_altura

    pid_tanque_1 = PID(1, 0.1, 0.05, setpoint=set_point_t1)
    pid_tanque_2 = PID(1, 0.1, 0.05, setpoint=set_point_t2)
#trocar para 0.05 e 0.025 para aumentar o tempo plotado

    while (aprox_equal(real_t1_altura,set_point_t1) == False) or (aprox_equal(real_t2_altura,set_point_t2) ==False) :
        print("atuador t1")
        print (atuador_t1)
        print("atuador t2")
        print (atuador_t1)

        array_atuador_1.append(atuador_t1)
        array_atuador_1.append(atuador_t1)
        array_atuador_2.append(atuador_t2)
        array_atuador_2.append(atuador_t2)

        if (aprox_equal(real_t1_altura,set_point_t1)) == False :
            mutex.acquire()  # Dá Chave para esta Thread
            try:
                atuador_t1 = pid_tanque_1(real_t1_altura)
            finally:
                mutex.release()  # Tira chave desta Thread

        if ((aprox_equal(real_t2_altura,set_point_t2)) == False) and (real_t1_altura> 0.5) : # Condição que tanque 1 tenha água
            mutex.acquire()  # Dá Chave para esta Thread
            try:
                atuador_t2 = pid_tanque_2(real_t2_altura)
            finally:
                mutex.release()  # Tira chave desta Thread
        event.wait(0.2)

def simula_tanque_1(vazão,altura,raio_base,raio_topo):

        global real_t1_altura,set_point_t1,atuador_t1,atuador_t2, array_altura_t_1  #Variáveis globais
        while  (aprox_equal(real_t1_altura,set_point_t1) == False) or (aprox_equal(real_t2_altura, set_point_t2)==False):



            numerador = atuador_t1 - (vazão * math.sqrt(real_t1_altura)) - atuador_t2
            denomidador = math.pi * pow((raio_base + ((raio_topo - raio_base) / altura) * real_t1_altura), 2)
            dif = numerador / denomidador

            # Dá Chave para esta Thread
            mutex.acquire()
            try:
                mutex.notify()
                real_t1_altura = (dif*0.1) + real_t1_altura
                real_t1_altura = max(0, real_t1_altura)  # certifica que a altura não é menor que zero
            finally:
                mutex.release() # Tira chave desta Thread
            array_altura_t_1.append(real_t1_altura)
            array_altura_t_2.append(real_t2_altura)
            event.wait(0.1)

    #    if (aprox_equal(real_t1_altura,set_point_t1)) & (aprox_equal(real_t2_altura, set_point_t2)):

            #print(process_thread_1.getName(), " acabou.")

def simula_tanque_2(vazão,altura,raio_base,raio_topo):
    global real_t2_altura, set_point_t2, atuador_t2 , array_altura_t_2,real_t1_altura,set_point_t1 # Passando as Variáveis globais para a função

    while ((aprox_equal(real_t2_altura, set_point_t2)) == False)  :
        numerador = atuador_t2 - (vazão * math.sqrt(real_t2_altura))
        denomidador = math.pi * pow((raio_base + ((raio_topo - raio_base) / altura) * real_t2_altura), 2)
        dif = numerador / denomidador
        mutex.acquire()  # Dá Chave para esta Thread
        mutex.notify()
        real_t2_altura = (dif*0.1) + real_t2_altura
        #real_t2_altura = max(0, real_t2_altura)  # certifica que a altura não é menor que zero
        mutex.notify()
        mutex.release() # Tira chave desta Thread
        event.wait(0.1)

    #if (aprox_equal(real_t2_altura, set_point_t2)) :
    #    print(process_thread_2.getName(), " acabou.")
