#!/usr/bin/env python

import iolPy

iol = iolPy.Iol()
iol.gestionar('AUTH')

# Descarga ultima cotizacion registrada de Grupo Galicia
json_res = iol.price_to_json('bcba', 'ggal')
print(json_res['ultimoPrecio'])

# Descarga cotizaciones de opciones de Grupo Galicia
# json_res = iol.descargar('opciones', 'ggal')
# print(json_res)

# Descarga panel general de acciones
# json_res = iol.descargar("panelGeneralAcciones")
# for linea in json_res['titulos']:
#     print("{:<10} {:<10} {:<10} {:<10}".format(linea['simbolo'],
#                                                linea['ultimoPrecio'],
#                                                linea['minimo'],
#                                                linea['maximo']))
