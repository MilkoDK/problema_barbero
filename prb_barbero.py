import threading
import time
import random

# Variables
CupoMaximo = 6
cant_clientes_espera = 0
despierto = False
cant_max_clientes = 12

# Controles para ordenar el orden de entrada y salida de los clientes
llega_cliente  =  threading.Semaphore(0)
cliente_terminado = threading.Semaphore(0)
paso = threading.Semaphore(0)
Babero_listo = threading.Semaphore(0) 
cliente_levantado = threading.Semaphore(0)
Cliente_listo = threading.Semaphore(0)


def cliente(id):
    global despierto
    global CupoMaximo
    global cant_clientes_espera
    time.sleep(random.uniform(0, 10))# Simula el tiempo que tarde un cliente en lleagr a la peluqueria.    
    if (despierto):
        if(cant_clientes_espera == CupoMaximo):
            print(f"El cliente {id} se retir por que no hay espacio en la peluqueria...")
            return
        else:
            cant_clientes_espera+=1
            print(f"El cliente {id} se sienta a esperar. Ocupa el puesto ({cant_clientes_espera} / {CupoMaximo})")
            paso.acquire()# Esperando el cliente en turno (en espera)
            cant_clientes_espera-=1
    else:
        print(f"Entra un cliente {id} y encuentra al barbero durmiendo")
        despierto = True
        llega_cliente.release()
        print("Despierta el barbero")
        # Le avisa al barbero que entro
    Babero_listo.acquire() 
    # Comienza a recortarse
    print(f"Cliente {id} se sienta en la silla.")
    Cliente_listo.release()
    print(f"El cliente {id} se esta recortando")
    cliente_terminado.acquire() # Esperamos a que el barbero nos recorte.
    print(f"El cliente {id} se levanta del asiento.")
    cliente_levantado.release()
    if(cant_clientes_espera >= 1):        
        print(f"El cliente {id} le aviso al otro que puede pasar.")
        paso.release()# Le aviso al otro cliente
    else:
        despierto=False
        print("El barbero se duerme porque no hay nadie. ZZZZZzzzzzz...")
        

def barbero():
    global despierto
    while True:
        if(despierto == False):
            llega_cliente.acquire()# Esperar a que un cliente entre (en espera)
        print("El barbero le indica al cliente que puede pasar.")
        Babero_listo.release()
        Cliente_listo.acquire() 
        print("El barbero esta ocupado")
        time.sleep(random.randint(1, 2))
        print("El barbero termina de recortar al cliente")
        cliente_terminado.release()# Le dice al cliente que termino de recortar (realizado)
        cliente_levantado.acquire()
        if(despierto == True):
            print("El barbero limpia el asiento.") # print del control barbero listo
    

hilos = []

Barbero = threading.Thread(target=barbero)
hilos.append(Barbero) # agrego hilo (barbero)

for t in range(cant_max_clientes):
    hilos.append(threading.Thread(target=cliente, args=(t,))) # Por cada cliente se agrega un hilo
    
for h in hilos:
    h.start() # por cada hilo se inicia el programa
        
for t in hilos:
    t.join() # Esperamos que cada hilo termine.


# Coloque el ID de cada cliente para facilitar la deteccion de bugs que presento mientras cre que codigo.   