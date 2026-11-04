
"""
Práctica tres: Modelado y control del sistema musculoesquelético

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Carolina Gamez Flores
Número de control: 23212193
Correo institucional: l23212193@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

import numpy as np
import math as m
import matplotlib.pyplot as plt
from scipy import signal
import control as ctrl
import pandas as pd

# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,10,5
N = round((tend-t0)/dt)+1
t = np.linspace(t0,tend,N)
u = np.zeros(N)
u[round(1/dt):round(2/dt)] = 1

# Componentes del circuito RC
def musculo(R):
    a,Cp,Cs = 0.25,100E-6,10E-6
    num = [Cs*R,1-a]
    den = [R*(Cs+Cp),1]
    sys = ctrl.tf(num,den)
    L = np.roots(den)
    return sys,L

# Función de transferencia de control
R = 100
sysControl,L = musculo(R)
print(f"Función de transferencia del control: {sysControl}")
print(f"Polos del sistema: L1 = {L[0]:.3e}\n")

# Función de transferencia de caso
R = 10E3
sysCaso,L = musculo(R)
print(f"Función de transferencia del caso: {sysCaso}")
print(f"Polos del sistema: L1 = {L[0]:.3e}\n")

# Respuesta del sistema en lazo abierto
_,Fsx = ctrl.forced_response(sysControl,t,u,x0)
_,Fsy = ctrl.forced_response(sysCaso,t,u,x0)

# Colores
clr1 = np.array([246,36,119])/255
clr2 = np.array([255,173,238])/255
clr3 = np.array([146,0,58])/255
clr4 = np.array([128,81,255])/255

# Controlador PI
def controlador(kI,kP,sys):
    Cr = 1E-6
    Re = 1/(Cr*kI)
    Rr = kP*Re
    numPID = [Rr*Cr,1]
    denPID = [Re*Cr,0]
    PID = ctrl.tf(numPID,denPID)
    sysPID = ctrl.feedback(ctrl.series(PID,sys),1,sign=-1)
    return sysPID

casoPID = controlador(41509.2699941618,0.0218624136400493,sysCaso)
print(f"Función de transferencia del sistema musculoesquelético en lazo cerrado: {casoPID}\n")

# Respuesta del sistema en lazo cerrado
_,PI = ctrl.forced_response(casoPID,t,Fsx,x0)

# Gráfica
fg = plt.figure(1)
fg.set_size_inches(w,h)
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Times New Roman'

plt.plot(t,u,'-',linewidth=0.7,color=clr1,label='F(t)')
plt.plot(t,Fsx,'-',linewidth=0.7,color=clr2,label='Fs(t): Control')
plt.plot(t,Fsy,':',linewidth=0.7,color=clr3,label='Fs(t): Caso')
plt.plot(t,PI,'--',linewidth=0.7,color=clr4,label='PID(t): Tratamiento')

plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.1,1.1); plt.yticks(np.arange(-0.1,1.11,0.1))
plt.xlabel('t[s]')
plt.ylabel('Fs(t) [V]')
plt.legend(bbox_to_anchor=(0.5,-0.25),loc='center',ncol=4,frameon=False)
fg.savefig('Caso_python.pdf',bbox_inches='tight')
plt.show()
