from datetime import datetime
from AESCipher.AESCipher import AESCipher
import json                         # Manejo de archivos json.
import requests                     # Requests HTTP post y get.
import csv

# Archivos
bearer_file = ".bearer"
cfg_file = '.params'
secret = '.secret'

# Crear el archivo .secret con la frase de encriptado. Mantener el archivo
# con los permisos minimos de lectura para el usuario local.
with open(secret, "rt") as sec_file:
    secret_phase = sec_file.read()

# Variables de Iol
# https://api.invertironline.com/Help
url_base = "https://api.invertironline.com/"
url_titulo_cot = "api/BCBA/Titulos/DICA/Cotizacion"
url_cot_panel_bonos = "api/Cotizaciones/bonos/PanelGeneral/Argentina"
url_cot_panel_acciones = "api/Cotizaciones/acciones/Panel%20General/argentina"
url_token = "token"
url_cot_opciones = {
    "GGAL": "/api/v2/BCBA/Titulos/GGAL/Opciones",
    "PAMP": "/api/v2/BCBA/Titulos/PAMP/Opciones",
}


# Clase para menejo de API iol
class Iol:

    def __init__(self):
        self.hora_actual = datetime.now()

        # Lectura de archivo de parametros
        try:
            with open(cfg_file, "rb") as binary_file:
                self.params = binary_file.read()

        except IOError:
            print("Archivo de parametros no encontrado...")
            exit()

    # Gestion de API tokens
    #
    # :param      type:     Tipo de gestion
    # :type       type:     { string }
    # :param      url:      Url para solicitar la operacion
    # :type       url:      { type_description }
    def gestionar(self, type, DEBUG=False):

        # Se descifra los parametros.
        cipher = AESCipher(secret_phase.encode("utf8"))  # Quitar
        payload = cipher.decrypt(self.params)

        if type == 'AUTH':

            url = url_base + url_token

            # Se abre archivo en busqueda de bearer.
            try:
                with open(bearer_file, "rt") as csv_file:
                    csvReader = csv.reader(csv_file,
                                           delimiter=',',
                                           quotechar='\"')
                    data_list = list(csvReader)

                    # Verificamos que el archivo no haya estado vacio.
                    if data_list == []:
                        print("Archivo .bearer vacio. Por favor eliminarlo.")
                        exit()

                    for row in data_list:
                        self.bearer = row[0]
                        self.refresh_token = row[1]
                        self.bearer_time = datetime.strptime(
                            row[2],
                            '%Y-%m-%d %H:%M:%S.%f')

                diferencia = (datetime.now() - self.bearer_time)

                if int(diferencia.total_seconds() / 60) < 16:
                    pass

                elif int(diferencia.total_seconds() / 60) > 30:
                    print("BNEW")

                    payload = "{" + payload + "}"
                    valor = json.loads(payload)

                    # Se hace peticion de bearer token a IOL.
                    req = requests.post(url, data=valor)

                    # Interpretamos respuesta y guardamos los resultados.
                    json_obj = json.loads(req.text)
                    self.bearer = json_obj['access_token']
                    self.refresh_token = json_obj['refresh_token']
                    self.bearer_time = datetime.now()

                    # Almacenando bearer.
                    with open(bearer_file, "wt") as csv_file:
                        csvWriter = csv.writer(csv_file)
                        csvWriter.writerow([self.bearer,
                                            self.refresh_token,
                                            self.bearer_time])

                else:
                    print("BVEN")

                    # Se convierten en json.
                    payload = "{" + "\"refresh_token\": \"" + self.refresh_token + "\", \"grant_type\": \"refresh_token\"" + "}"
                    valor = json.loads(payload)

                    # Se hace peticion de bearer token a IOL.
                    req = requests.post(url, data=valor)

                    # Interpretamos respuesta y guardamos los resultados.
                    json_obj = json.loads(req.text)

                    self.bearer = json_obj['access_token']
                    self.refresh_token = json_obj['refresh_token']
                    self.bearer_time = datetime.now()

                    # Almacenando bearer.
                    with open(bearer_file, "wt") as csv_file:
                        csvWriter = csv.writer(csv_file)
                        csvWriter.writerow([self.bearer,
                                            self.refresh_token,
                                            self.bearer_time])

            except IOError:
                print("BERR - Bearer no encontrado. Generando uno nuevo...")

                # Se convierten en json.
                payload = "{" + payload + "}"
                valor = json.loads(payload)

                # Se hace peticion de bearer token a IOL.
                req = requests.post(url, data=valor)

                # Interpretamos respuesta y guardamos los resultados.
                if req.status_code == 200:
                    json_obj = json.loads(req.text)

                    self.bearer = json_obj['access_token']
                    self.refresh_token = json_obj['refresh_token']
                    self.bearer_time = str(datetime.now())

                    # Almacenando bearer.
                    with open(bearer_file, "wt") as csv_file:
                        csvWriter = csv.writer(csv_file)
                        csvWriter.writerow([self.bearer,
                                            self.refresh_token,
                                            self.bearer_time])
                        print("Archivo bearer creado.")

                else:
                    print(req.status_code, req.text)

    # Funcion: Descargar()
    #
    # Parametros:
    # panelGeneralAcciones  -> Obtenemos cotizaciones de panel general de
    #                          acciones.
    # panelGeneralBonos     -> Obtenemos cotizaciones de panel general de
    #                          bonos.
    # opciones              -> Obtenemos cotizaciones de las distintas bases
    #                          de opciones de un subyacente x.
    def descargar(self, solicitud, activo=None):

        print("Obteniendo: ", solicitud)
        print("Sobre: ", activo)

        # Verificamos validez del bearer
        diferencia = (datetime.now() - self.bearer_time)
        if int(diferencia.total_seconds() / 60) < 14:

            # Chequeamos que queremos obtener
            if solicitud == "panelGeneralAcciones":
                url = url_base + url_cot_panel_acciones
                req = requests.get(
                    url,
                    headers={"Authorization": "Bearer " + self.bearer})
            elif solicitud == "panelGeneralBonos":
                url = url_base + url_cot_panel_bonos
                req = requests.get(
                    url,
                    headers={"Authorization": "Bearer " + self.bearer})
            elif solicitud == "opciones":
                url = url_base + url_cot_opciones[activo.upper()]
                req = requests.get(
                    url,
                    headers={"Authorization": "Bearer " + self.bearer})
            return json.loads(req.text)

    # Descarga de ultima cotizacion
    # :param      mercado:  Mercado donde opera el titulo
    # :type       mercado:  str { bcba/nyse/nasdaq }
    # :param      titulo:   Titulo a consultar
    # :type       titulo:   str
    # :returns:   Json con 'ultimoPrecio', 'variacion', 'apertura', 'maximo',
    #             'minimo', 'fechaHora', 'tendencia', 'cierreAnterior',
    #             'montoOperado', 'volumenNominal', 'precioPromedio', 'moneda',
    #             'precioAjuste', 'interesesAbiertos', 'puntas',
    #             'cantidadOperaciones
    # :rtype:     json object
    def price_to_json(self, mercado='bcba', simbolo=None):

        url = url_base + "api/v2/" +\
            mercado + "/Titulos/" + simbolo + "/Cotizacion"
        req = requests.get(
            url,
            headers={"Authorization": "Bearer " + self.bearer})
        return json.loads(req.text)

    # Descarga de valores temporales para periodo particular
    # :param      mercado:  Mercado
    # :type       mercado:  str
    # :param      titulo:   Titulo
    # :type       titulo:   str
    # :returns:   Cotizacion historica del periodo especificado para el titulo
    # :rtype:     Json_object
    def hist_price_to_json(self, mercado='bcba', simbolo=None,
                           desde=None, hasta=None):

        url = url_base + "api/v2/" + mercado + "/Titulos/" + simbolo +\
            "/Cotizacion/seriehistorica/" + desde + "/" + hasta + "/ajustada"
        req = requests.get(
            url,
            headers={"Authorization": "Bearer " + self.bearer})
        if req.status_code == 200:
            return json.loads(req.text)
        else:
            print("ERR -", req.status_code, req.text)
            return False
