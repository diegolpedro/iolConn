#!/usr/bin/env python
#
# iolConn es un conector python para la API Invertir Online -
# api.invertironline.com.ar
#
# iolConn is an API connector for Invertir Online -
# api.invertironline.com.ar
#
# Copyright (c) 2023 Diego L. Pedro <diegolpedro@gmail.com>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from iolConn import Iol
from getpass import getpass


def example_one_price(iol):

    # Descarga ultima cotizacion registrada de Grupo Galicia
    json_res = iol.price_to_json('bcba', 'ggal')
    print(json_res['ultimoPrecio'])


def example_options(iol):

    # Descarga cotizaciones de opciones de Grupo Galicia
    json_res = iol.descargar('opciones', 'ggal')
    print(json_res)


def example_panel(iol):

    # Descarga panel general de acciones
    json_res = iol.descargar("panelGeneralAcciones")
    for linea in json_res['titulos']:
        print("{:<10} {:<10} {:<10} {:<10}".format(linea['simbolo'],
                                                   linea['ultimoPrecio'],
                                                   linea['minimo'],
                                                   linea['maximo']))


if __name__ == '__main__':

    user = input("Ingrese usuario: ")
    pwd = getpass("Ingrese password: ")

    iol = Iol(user, pwd)
    if iol.gestionar():
        exit()

    example_one_price(iol)
    # example_panel(iol)
    # example_options(iol)
