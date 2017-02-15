#!/usr/bin/python3

"""
Miguel Ángel Lozano Montero.
Programa que construye una aplicación web que suma en dos fases.
"""

import socket

# Create a TCP objet socket and bind it to a port
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Let the port be reused if no process is actually using it
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the address corresponding to the main name of the host
mySocket.bind((socket.gethostname(), 1234))

# Queue a maximum of 5 TCP connection requests

mySocket.listen(5)

# Accept connections, read incoming data, and answer back an HTML page
# (in an almost-infinite loop; the loop can be stopped with Ctrl+C)

sumandos = []

try:
    while True:
        print('Waiting for connections')
        (recvSocket, address) = mySocket.accept()
        print('Request received:')
        # bytes => utf-8
        peticion = recvSocket.recv(2048).decode("utf-8", "strict")
        print(peticion)
        # Nos quedamos con el recurso
        recurso = peticion.split()[1][1:]

        if recurso == "favicon.ico":
            recvSocket.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n" +
                                  "<html><body><h1>Not Found" +
                                  "</h1></body></html>\r\n", "utf-8"))
            recvSocket.close()
            # Lleva a la siguiente iteración del bucle
            continue
        else:
            try:
                # Comprobamos que metemos un número como recurso
                sumandos.append(int(recurso))
            except ValueError:
                # Si no es un entero, mandamos un mensaje de error
                recvSocket.send(bytes("HTTP/1.1 400 Bad Request\r\n\r\n" +
                                      "<html><body><h1>No me has dado" +
                                      " un entero. Vete." +
                                      "</h1></body></html>\r\n", "utf-8"))
                recvSocket.close()
                continue

        if len(sumandos) == 1:
            recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n" +
                                  "<html><body><h1>Me has dado un " +
                                  str(sumandos[0]) + ". Dame mas." +
                                  "</h1></body></html>\r\n", "utf-8"))
            recvSocket.close()
        else:   # Si no hay un 1 elemento en la lista, habrá 2
            suma = sumandos[0] + sumandos[1]
            recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n" +
                                  "<html><body><h1>Me habias dado un " +
                                  str(sumandos[0]) + ". Ahora un " +
                                  str(sumandos[1]) + ". Suman " +
                                  str(suma) + "." +
                                  "</h1></body></html>\r\n", "utf-8"))
            sumandos.clear()    # Vacíamos la lista tras mostrar la suma
            recvSocket.close()

except KeyboardInterrupt:
    print()
    print("Closing binded socket")
    mySocket.close()
