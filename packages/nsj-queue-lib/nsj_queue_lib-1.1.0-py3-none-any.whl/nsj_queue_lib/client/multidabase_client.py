import requests
from nsj_queue_lib.settings import (
    MULTI_DATABASE_USER,
    MULTI_DATABASE_PASSWORD,
    MULTI_DATABASE_CLIENT_ID,
)


class MultiDatabaseClient:
    def __init__(self):
        self.url = "https://api.sre.nasajon.com.br/erp/credentials"
        self.token = self._retrieve_token()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _retrieve_token(self):
        auth_url = "https://auth.nasajon.com.br/auth/realms/master/protocol/openid-connect/token"
        auth_payload = {
            "username": MULTI_DATABASE_USER,
            "password": MULTI_DATABASE_PASSWORD,
            "client_id": MULTI_DATABASE_CLIENT_ID,
            "scope": "offline_access",
            "grant_type": "password",
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        try:
            response = requests.post(auth_url, data=auth_payload, headers=headers)
            response.raise_for_status()
            return response.json().get("access_token")
        except requests.exceptions.RequestException as e:
            raise Exception(
                f"Erro ao recuperar o token para chamada à API multibanco: {e}"
            )

    def get_erp_credentials(self, tenant):
        payload = {"tenant": tenant}
        try:
            response = requests.post(self.url, json=payload, headers=self.headers)
            response.raise_for_status()  # Levanta um erro para respostas com status 4xx/5xx
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao chamar a API: {e}")


if __name__ == "__main__":
    client = MultiDatabaseClient()
    credentials = client.get_erp_credentials(tenant=47)
    if credentials:
        print("Resposta da API:", credentials)
