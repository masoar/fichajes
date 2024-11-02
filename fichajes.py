from flask import Flask, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

# Configuración de la hoja de cálculo
SPREADSHEET_ID = '1wdtIZYNhj1N_yAI7EF1xAblTxSJ9edx6qchMn4z_SI4'  # Reemplaza con el ID de tu hoja
RANGE_NAME = 'Fichajes!A:D'

# Autenticación con Google Sheets API
credentials = service_account.Credentials.from_service_account_file(
    'credentials.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)

# Conectar con Google Sheets
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

# Configuración de la app Flask
app = Flask(__name__)

# Endpoint para registrar fichajes
@app.route('/fichar', methods=['POST'])
def registrar_fichaje():
    # Obtener datos del cuerpo de la solicitud
    data = request.get_json()
    id_empleado = data.get('id_empleado')
    tipo = data.get('tipo')  # "Entrada" o "Salida"
    
    # Obtener fecha y hora actuales
    fecha = datetime.now().strftime('%Y-%m-%d')
    hora = datetime.now().strftime('%H:%M:%S')
    datos = [[id_empleado, fecha, hora, tipo]]
    body = {'values': datos}

    # Insertar datos en Google Sheets
    try:
        result = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        return jsonify({"status": "success", "message": "Fichaje registrado correctamente"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
