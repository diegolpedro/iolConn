iolPy - Conector API de Iol
===========================
![PyPI pyversions](https://img.shields.io/badge/python-3.7+-blue.svg?style=flat)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/diegolpedro)

Preparación
-----------
### Seteo del entorno
Para utilizar el conector primero preparar un entorno de ejecución. En este caso se utilizó Anaconda y Python 3.7.
```
conda create -n "\<nombre\>" python==3.7
conda activate \<nombre\>
```
Una vez dentro del entorno, instalamos los requisitos.
```
pip3 install -r requirements.txt
```
### Seteo del conector
Se debe primero crear un archivo en el directorio raíz con el nombre .secret y allí almacenar un clave secreta de encriptación. Es importante mantener el nombre del archivo y los permisos limitados para lectura del usuario local.
```
echo "clavesecretadeenciptacion" > .secret
```
Una vez que se tenga este archivo, se debe correr 'params.py' con la opción -c y el nombre de usuario. Se le pedirá el password para almacenarla cifrada dentro del archivo .params.
```
python3 params.py -c <usuario_iol>
```
Utilización
-----------
Se puede encontrar un ejemplo de uso dentro del archivo test.py. El mismo traerá desde la API de Iol, la última cotización de Grupo Galicia en el mercado de Buenos Aires.
```
python3 test.py
```
Conector
-----------
El conector solo gestiona los bearings correspondientes, reutiliza los gestionados y renueva los vencidos. Consta de una clase que debe instanciarse para utilizar las distintas funcionalidades. Las funciones al día de hoy son:
```
gestionar(type, DEBUG=False)                        # Gestion de API tokens.
descargar(solicitud, activo=None)                   # Descargar lotes de cotizaciones.
price_to_json(mercado='bcba', simbolo=None)         # Descargar ultima cotizacion de un simbolo.
hist_price_to_json(mercado='bcba', simbolo=None,    # Descarga de valores temporales para periodo 
                   desde=None, hasta=None)          # particular.
```
### Opciones
Mercados al 08/06/21
- bCBA
- nYSE
- nASDAQ
- aMEX 
- bCS
- rOFX 

### Solicitudes para función descargar
- panelGeneralAcciones  -> Obtenemos cotizaciones de panel general de acciones.
- panelGeneralBonos     -> Obtenemos cotizaciones de panel general de bonos.
- opciones              -> Obtenemos cotizaciones de las distintas bases de opciones de un subyacente x.

### Fechas
- Fechas en formato 2023-07-23
