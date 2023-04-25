from ..request import API_connection
from fastapi import HTTPException
from datetime import date
import requests
import json


def return_FPO_data():

    #FDF = Fecha_Desde_FPO.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    #FHF = Fecha_Hasta_FPO.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    url = 'https://apps09mdc-back-projectsprd.azurewebsites.net/api/v1/TransmissionProjects/Search'
    headers = {
        'accept': '*/*', 
        'Authorization': API_connection.return_token_data(), 
        'Content-Type': 'application/json-patch+json'
        }
    body = {"startDateFpo": "1900-01-01T00:00:00.000Z", "endDateFpo": "3000-01-01T00:00:00.000Z"}

    r = requests.post(url, headers=headers, json=body)

    if (r.status_code == 200):
        j = r.json()
        d = [{  
            'Codigo_Proyecto' : item['projectRidModified'],
            'FPO_Oficial' : item['fpoOfficial'],
            'FPO_Real' : item['projectFpo']} for item in j['items']]
        return d
    else:
        raise HTTPException(status_code = 400, detail = f"Problemas de Conexión a la API Proyectos. Error: {str(r)}")