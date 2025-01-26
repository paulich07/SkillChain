import requests

# ======== CONFIGURAZIONE =========
BASE_URL = "http://127.0.0.1:8000/api/auth"
REGISTER_URL = f"{BASE_URL}/register/"
LOGIN_URL = f"{BASE_URL}/login/"
LOGOUT_URL = f"{BASE_URL}/logout/"
ME_URL = f"{BASE_URL}/profile/"

# ✅ Credenziali di test
TEST_USERNAME = "newuser"
TEST_PASSWORD = "StrongPass123"
TEST_EMAIL = "newuser@example.com"

session = requests.Session()  # Creiamo una sessione persistente

def register():
    """Registra un nuovo utente"""
    payload = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD,
        "email": TEST_EMAIL,
        "first_name": "John",
        "last_name": "Doe",
    }
    
    response = session.post(REGISTER_URL, json=payload)
    print_response("🔹 REGISTRAZIONE", response)

def login():
    """Esegue il login e imposta i token di autenticazione"""
    payload = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD,
    }
    
    response = session.post(LOGIN_URL, json=payload)
    print_response("🔹 LOGIN", response)
    
    if response.status_code == 200:
        # ✅ Recuperiamo il token CSRF e il session ID
        csrf_token = response.json().get("csrf_token")
        session.headers.update({"X-CSRFToken": csrf_token})  # Aggiungiamo il CSRF nelle intestazioni
        return csrf_token
    return None

def get_user():
    """Recupera i dati dell'utente autenticato"""
    response = session.get(ME_URL)
    print_response("🔹 DATI UTENTE", response)

def update_user():
    """Modifica i dati dell'utente autenticato"""
    data = {"first_name": "Johnny", "last_name": "Doe Updated"}
    
    response = session.patch(ME_URL, json=data)
    print_response("🔹 MODIFICA DATI UTENTE", response)

def logout():
    """Effettua il logout"""
    response = session.post(LOGOUT_URL)
    print_response("🔹 LOGOUT", response)

def print_response(action, response):
    """Stampa i risultati"""
    print(f"\n{action} - Status Code: {response.status_code}")
    try:
        print("Response JSON:", response.json())
    except Exception:
        print("Response Text:", response.text)

# ======== ESECUZIONE TEST =========
if __name__ == "__main__":
    register()
    
    csrf_token = login()
    if csrf_token:
        get_user()
        update_user()
        logout()