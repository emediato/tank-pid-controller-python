from threading import  Lock
import threading
from threading import Condition
import math
import time
from simple_pid import PID
import matplotlib.pyplot as plt
import numpy as np
from threading import Thread
from GVL import *
from var import *

lock = threading.RLock()
mutex = Condition(lock)
event = threading.Event()



if __name__ == "__main__":
    # creating thread
    process_thread_1 = threading.Thread(target=simula_tanque_1,name='Processo tanque 1' ,args=(0.8,5,1,2))
    process_thread_2 = threading.Thread(target=simula_tanque_2,name='Processo tanque 2' ,args=(0.5,3,0.5,1))
    controler =   threading.Thread(target=control,name='Controlador' )

    # starting thread 1
    process_thread_1.start()

    # starting thread 2
    process_thread_2.start()

    #Starting Controler
    controler.start()

    # wait until thread 1 is completely executed
    process_thread_1.join()
    # wait until thread 2 is completely executed
    process_thread_2.join()
    # wait until controler is completely executed
    controler.join()

    # both threads completely executed
    print("\nDone!")


    fig , ax  =plt.subplots(2)

    ax[0].set_title('Altura dos tanques')
    ax[0].plot(np.arange(0,len(array_altura_t_1),1),array_altura_t_1,label='Altura tanque 1',color='red')

    ax[0].axhline(set_point_t1, linewidth=0.5,color='red',label='Set_point_1',alpha=0.6)

    ax[0].set_xlabel('Tempo em segundos')
    ax[0].plot(np.arange(0, len(array_altura_t_2), 1), array_altura_t_2,label='Altura tanque 2',color='green')
    ax[0].axhline(set_point_t2, linewidth=0.5,color='green',label='Set_point_2',alpha=0.6)
    ax[0].legend(loc='upper left')

    ax[1].set_title('Atuadores dos tanques')
    ax[1].plot(np.arange(0, len(array_atuador_1), 1)/10, array_atuador_1, label='Atuador 1',color='red')
    ax[1].plot(np.arange(0, len(array_atuador_2), 1)/10, array_atuador_2, label='Atuador 2',color='green')
    ax[1].legend(loc='upper left')
    ax[1].set_xlabel('Tempo em segundos')

    #time = len(array_altura_t_1)
    #time2 = len(array_altura_t_2)
    #fig = plt.figure()
    #ax1 = fig.add_subplot()
    #ax1.plot((0, time), array_atuador_1)
    #ax1.plot((0, time2), array_altura_t_2)
    #ax1.set_xlabel('Time')
    #ax1.set_ylabel('Control')
    plt.tight_layout()
    #plt.show()

    #fig, (ax0, ax1) = plt.subplots(2, 1, constrained_layout=True)
    #ax0.plot(0, len(array_altura_t_1), array_altura_t_1, label="a1")
#    ax0.plot(0, len(array_altura_t_2), array_altura_t_2, label=" a2")
#    ax0.legend(shadow=True, fancybox=True)
#    leg = ax0.legend(loc="upper left", bbox_to_anchor=[0, len(array_altura_t_1)],
#                 ncol=2, shadow=True, title="level tank", fancybox=True)
#    leg.get_title().set_color("red")

#    ax1.plot(0, array_atuador_1, label=r" a1 ")
#    ax1.plot(0, array_atuador_2, label=" a2")
#    ax1.legend(shadow=True, fancybox=True)

    plt.show()
