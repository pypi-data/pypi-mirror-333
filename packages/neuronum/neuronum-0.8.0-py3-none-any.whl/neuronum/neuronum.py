import requests
from typing import Optional


class Cell:
    def __init__(self, host: str, password: str, network: str, synapse: str):
        self.host = host
        self.password = password
        self.network = network
        self.synapse = synapse

    def to_dict(self) -> dict:
        return {
            "host": self.host,
            "password": self.password,
            "synapse": self.synapse
        }

    def __repr__(self) -> str:
        return f"Cell(host={self.host}, password={self.password}, network={self.network}, synapse={self.synapse})"

    def activate(self, txID: str, data: dict, base_url: str = "http://{network}/activateTX"):
        full_url = base_url.format(network=self.network) + f"/{txID}"

        TX = {
            "data": data,
            "cell": self.to_dict()
        }

        try:
            response = requests.post(
                full_url,
                json=TX,
            )

            response.raise_for_status()

            print(f"Response from FastAPI backend: {response.json()}")

        except requests.exceptions.RequestException as e:
            print(f"Error sending request: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")



    def test_connection(self, base_url: str = "http://{network}/testConnection"):
            full_url = base_url.format(network=self.network)

            TX = {
                "host": self.host,
                "password": self.password,
                "synapse": self.synapse
            }

            print(TX)

            try:
                response = requests.post(
                    full_url,
                    json=TX, 
                )

                response.raise_for_status()
                print(f"Response from FastAPI backend: {response.json()}")

            except requests.exceptions.RequestException as e:
                print(f"Error sending request: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")




    def store(self, label: str, data: dict, ctx: Optional[str] = None):
        if ctx:
            full_url = f"http://{self.network}/store_ctx/{ctx}"
        else:
            full_url = f"http://{self.network}/store"
        
        store = {
            "label": label,
            "data": data,
            "cell": self.to_dict()  
        }

        try:
            response = requests.post(full_url, json=store)
            response.raise_for_status()
            print(f"Response from FastAPI backend: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending request: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")



    def load(self, label: str, ctx: Optional[str] = None):
        if ctx:
            full_url = f"http://{self.network}/load_ctx/{ctx}"
        else:
            full_url = f"http://{self.network}/load"
        
        print(f"Full URL: {full_url}")

        load = {
            "label": label,
            "cell": self.to_dict() 
        }

        try:
            response = requests.post(full_url, json=load)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending request: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")



    def delete(self, label: str, ctx: Optional[str] = None):
        if ctx:
            full_url = f"http://{self.network}/delete_ctx/{ctx}"
        else:
            full_url = f"http://{self.network}/delete"
        
        print(f"Full URL: {full_url}")

        delete = {
            "label": label,
            "cell": self.to_dict() 
        }

        try:
            response = requests.post(full_url, json=delete)
            response.raise_for_status()
            print(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error sending request: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


__all__ = ['Cell']
