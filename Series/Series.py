'''
#Inicializa variables
x = 1
y = 1
print(x,y)

while (x<10):
    #Guarde en z la suma de x,y
    z = x + y
    #Aumente x en 1
    x = x + 1
    #Guarde en y la suma de x, y anteriores junto con el x actual
    y = x + z
    print(x,y)
'''

#Inicializa variables
x = 1
y = 1
print(x,y)

while(x<10):
    #Guarde en y la suma de x, y anterior
    y = x + y
    #Aumente x en 1
    x = x + 1
    #Guarde la suma de x,y anteriores junto con el x actual
    y = y + x
    print(x,y)
