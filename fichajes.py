import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Función auxiliar para cargar variables de entorno o devolver un valor por defecto
def get_env_var(var_name, default=""):
    value = os.getenv(var_name)
    if value is None:
        print(f"Warning: {var_name} no está definido")
    return value or default

# Crear el diccionario de credenciales usando las variables de entorno
credentials_info = {
    "type": get_env_var("GCP_TYPE"),
    "project_id": get_env_var("GCP_PROJECT_ID"),
    "private_key_id": get_env_var("GCP_PRIVATE_KEY_ID"),
    "private_key": get_env_var("GCP_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": get_env_var("GCP_CLIENT_EMAIL"),
    "client_id": get_env_var("GCP_CLIENT_ID"),
    "auth_uri": get_env_var("GCP_AUTH_URI"),
    "token_uri": get_env_var("GCP_TOKEN_URI"),
    "auth_provider_x509_cert_url": get_env_var("GCP_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": get_env_var("GCP_CLIENT_X509_CERT_URL"),
}

# Usar el diccionario de credenciales para autenticarse
credentials = service_account.Credentials.from_service_account_info(credentials_info)
service = build('sheets', 'v4', credentials=credentials)