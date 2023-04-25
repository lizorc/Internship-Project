from fastapi import HTTPException
import requests


def return_token_data():
    url = 'https://xmze2gaoprdappf04.azurewebsites.net/api/Autenticacion/GenerarToken?aplicacionToken=C7D1E7EB-6F59-401F-BBD4-1D584BAA07B7'
    headers = {
        'accept': '*/*', 
        'api-version': '2',
        'Content-Type': 'application/json'
        }
    body = {
        "idObjeto": "bd7d57a0-7e1e-4d11-b91a-fc841efeeb9a",
        "nombre": "PC_INDICADORES_LIQUIDACION_XM",
        "nombreCompleto": "PC_INDICADORES_LIQUIDACION_XM",
        "correoElectronico": "PC_INDICADORES_LIQUIDACION_XM@XM.COM.CO"
        }

    r = requests.post(url, headers=headers, json=body)

    if (r.status_code == 200):
        j = r.json()
        return ('Bearer  '+ j['token'])
    else:
        raise HTTPException(status_code = 400, detail = f"Problemas de Conexión a la API Proyectos. Error: {str(r)}")