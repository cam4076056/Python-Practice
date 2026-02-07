import tkinter
from tkinter import PhotoImage
from PIL import Image,ImageTk
import numpy as np
import threading
from functools import partial
import sys,time
import os
    
#Clase posicion
#Coordenadas en las que se encuentra el caballo. 
class posicion():
    #Variables "x" y "y" para las posiciones. 
    x=0
    y=0
    
    #Inicializa la posición del caballo - parametros "x" y "y".
    def __init__(self,x,y):
            self.x=x
            self.y=y
    
    #Función llamada "siguiente". Genera una lista con todas las posibilidades que tiene el caballo para avanzar. 
    #Parametro "posicion" - return lista
    def siguiente(p):
        lista = []
        x=p.x
        y=p.y
        if(x - 2 >= 0 and y - 1 >= 0):
            p1=posicion(x-2,y-1)
            lista.append(p1)
        if (x - 1 >= 0 and y - 2 >= 0) :
            p1=posicion(x - 1, y - 2)
            lista.append(p1)
        if (x + 1 < 8 and y - 2 >= 0):
            p1=posicion(x + 1, y - 2)
            lista.append(p1)
        if (x + 2 < 8 and y - 1 >= 0):
            p1=posicion(x + 2, y - 1)
            lista.append(p1)
        if (x + 2 < 8 and y + 1 < 8):
            p1=posicion(x + 2, y + 1)
            lista.append(p1)
        if (x + 1 < 8 and y + 2 < 8):
            p1=posicion(x + 1, y + 2)
            lista.append(p1)
        if (x - 1 >= 0 and y + 2 < 8):
            p1=posicion(x - 1, y + 2)
            lista.append(p1)
        if (x - 2 >= 0 and y + 1 < 8) :
            p1=posicion(x - 2, y + 1)
            lista.append(p1)
        return lista

#Clase tablero
class Tablero(threading.Thread):
    
    #Inicializamos 5 variables.
    x=0
    y=0
    tablero=np.zeros((8,8))
    visitado=[False]*64    
    fin=False
    
    #Constructor que inicializa el tablero.
    def __init__(self,sleep_interval=1):
        threading.Thread.__init__(self)
        self._kill = threading.Event()
        self._interval = sleep_interval
    def inicial(self,x,y):
        self.x=x
        self.y=y
    
    #Método que recibe una posición x-y y paso.
    def algoritmo(self,fila,columna,paso):
        #Busca si la fila y el tablero aparecen como visitadas. Multiplica la fila por tablero.
        self.visitado[fila * 8 + columna] = True
        #Cuenta los pasos dependiendo de la posición. 
        self.tablero[fila][columna] = paso
        #Genera una nueva posición + la posición en este momento. 
        p = posicion(columna, fila)
        #Genera una lista de posiciones "siguiente" con el método en posición p. 
        siguiente = posicion.siguiente(p);
        #Descarta las posiciones que posiblemente se tengan. 
        while (len(siguiente)!=0):
            is_killed = self._kill.wait(self._interval)
            if is_killed:
                break
            h = siguiente.pop(0);
            if (self.visitado[h.y * 8 + h.x]==False):
                self.algoritmo(h.y, h.x, paso + 1)
        #Valida si el paso es menor al visitado y si no ha llegado al fin. 
        if (paso < 64 and self.fin==False):
            self.tablero[fila][columna] = 0
            self.visitado[fila * 8 + columna] = False;
        else:
            self.fin = True 
    
    #Método que muestra la matriz en la consola. 
    def show(self):
        print(self.tablero)
    def kill(self):
        self._kill.set()
    #Ejecuta la función algoritmo. 
    def run (self):
        self.algoritmo(self.x,self.y,1)

#Clase actualizador
#Actualiza el tablero en un ciclo while cada uno de los botones de la lista. 
class Actualizador(threading.Thread):
    listab=[]
    #Constructor que inicializa el tablero.
    def __init__(self,lista,sleep_interval=1):
        threading.Thread.__init__(self)
        self.listab=lista
        self._kill = threading.Event()
        self._interval = sleep_interval
    def run (self):
        while(True):
            #Recorre el tablero cada vez que encuentre un número !0.
            #Reemplaza el icono por bacallo2.png y el texto al número del tablero en donde esté. 
            t=Tablero.tablero
            for i in range(8):
                for j in range(8):
                    if(t[i][j]!=0):
                        g=i*8+j
                        b=listab[g]
                        if(b['text']==""):
                            b.configure(text=int(t[i][j]),image=img, compound="top")
                    else:
                        g=i*8+j
                        b=listab[g]
                        b.configure(text="",image="")
            is_killed = self._kill.wait(self._interval)
            if is_killed:
                break
    
    def kill(self):
        self._kill.set()
                            
#Clase GUI
#Se diseña y desarrolla el tablero con sus respectivas medidas e imagenes. 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_img = os.path.join(BASE_DIR, "caballo.jpg") # Busca la imagen en la misma carpeta del programa.
root = tkinter.Tk()  
root.geometry("600x600")
img = Image.open(ruta_img)
img = img.resize((20, 20), Image.ANTIALIAS) # Redimension (Alto, Ancho)
img = ImageTk.PhotoImage(img)
listap = []
listab = []
T = Tablero()
A=Actualizador(listab)

#Método que activa los dos hilos, apaga e inicializa. 
def set(x,y):
    for b in listab:
        b["state"] = "disabled"
    T.inicial(x,y)
    A.start()
    T.start()
#Apaga los botones del arreglo para evitar que el usuario los presione.
def acabar():
    A.kill()
    T.kill()
for i in range(8):
    for j in range(8):
        label = tkinter.LabelFrame(root, width=64, height=64)
        label.grid(row=i, column=j)
        label.grid_rowconfigure(0, weight=1)
        label.grid_columnconfigure(0, weight=1)
        label.grid_propagate(False)
        if(i%2==0 and j%2==0)or(j%2==1 and i%2==1) :
            #Se le asigna el color a la casilla, en este caso blanca.
            b = tkinter.Button(label,bg='White',command=partial(set,i,j))
            b.grid(row=0, column=0, sticky='nesw')
        else:
            #Se le asigna el color a la casilla, en este caso dorada.
            b = tkinter.Button(label,bg='gold', command=partial(set,i,j))
            b.grid(row=0, column=0, sticky='nesw')
        listab.append(b) 
#Se crea el botón "Cancelar" para que termine el proceso. 
terminar = tkinter.Button(root,bg='White',height = 2, 
                  width = 7, command=acabar,text="Cancelar ")
terminar.grid(row=9, column=0)
root.mainloop()



