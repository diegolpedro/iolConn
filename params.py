#!/usr/bin/python
from AESCipher.AESCipher import AESCipher   # AES cypher.
from getpass import getpass
import sys


# Variables de cifrado (Cypher)
# Colocar en un archivo nombrado .secret la cadena de cifrado
with open(".secret", "r") as secret_file:
    secret = secret_file.read().replace('\n', '')
cipher = AESCipher(secret)  # Cadena para cifrado de usuario y password.

# Variables de configuracion
cfg_file = '.params'  # Nombre del archivo de parametros.


def mostrar_ayuda():
    print(
        """
        AYUDA:
        Params permite cifrar mediante el algoritmo AES y una clave de cifrado
        el usuario y password de la cuenta de Iol.

        IMPORTANTE: Nunca compartir ni hacer publico el archivo generado
        ==========  (.secret). Mantener con los permisos minimos de lectura.


        $ ./params.py [options]

        Options
        =======
        --help/-h       -> Esta ayuda.
        -c <usr>        -> Crea archivo de clave cifrado.
                           <usr> usuario de Iol
                           <pass> password de Iol
        """)


if __name__ == '__main__':

    # Interprete los argumentos.
    if len(sys.argv) > 1:
        if sys.argv[1] == '-c' and len(sys.argv) == 3:
            pwd = getpass()
            # Crea archivo de parametros.
            # Si se utiliza -c, se genera el archivo de parametros.
            with open(cfg_file, "wb") as binary_file:
                cadena = '\"username\": \"' + sys.argv[2] + '\", \"password\": \"' + pwd + '\", \"grant_type\": \"password\"'
                binary_file.write(cipher.encrypt(cadena))
                print(' --> Archivo generado.')
                exit()

        else:
            print('\n --> Opcion incorrecta.')

    mostrar_ayuda()
