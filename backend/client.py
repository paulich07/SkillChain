import requests

# ======== CONFIGURAZIONE =========

BASE_URL = "http://127.0.0.1:8000/api"  # Cambia se il server è su un altro host
LOGIN_URL = f"{BASE_URL}/auth/login/"
LOGOUT_URL = f"{BASE_URL}/auth/logout/"

session = requests.Session()  # Sessione globale per mantenere autenticazione


# ======== FUNZIONI DI AUTENTICAZIONE =========

def login(username, password):
    """Autenticazione con sessione e gestione CSRF token"""
    payload = {"username": username, "password": password}
    response = session.post(LOGIN_URL, json=payload)

    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"❌ Errore di login - Risposta non JSON:\n{response.text}")
        return False

    if response.status_code != 200:
        print(f"❌ Errore di login: {response_json}")
        return False

    # Salviamo il CSRF token ricevuto dal server
    csrf_token = response_json.get("csrf_token")
    if csrf_token:
        session.headers.update({"X-CSRFToken": csrf_token})
    
    print("✅ Login effettuato con successo!")
    return True


def logout():
    """Effettua il logout e chiude la sessione"""
    response = session.post(LOGOUT_URL)
    print_response(response)


# ======== FUNZIONI PER LE API =========

def get_events():
    """Recupera tutti gli eventi"""
    response = session.get(f"{BASE_URL}/events/")
    print_response(response)

def create_event():
    """Crea un nuovo evento"""
    data = {
        "name_event": "Hackathon Web3",
        "start_date": "2025-02-15T10:00:00Z",
        "end_date": "2025-02-15T18:00:00Z",
        "description": "Evento per sviluppatori blockchain."
    }
    response = session.post(f"{BASE_URL}/events/", json=data)
    print_response(response)

def add_badge_to_event(event_id):
    """Aggiunge un badge a un evento esistente"""
    data = {
        "badges": [
            {"name": "Badge Partecipazione", "event_name": "Hackathon Web3", "cid": "Qm123..."}
        ]
    }
    response = session.post(f"{BASE_URL}/events/{event_id}/badges/", json=data)
    print_response(response)

def update_badge(event_id, badge_id):
    """Modifica un badge di un evento"""
    data = {
        "name": "Badge VIP"
    }
    response = session.patch(f"{BASE_URL}/events/{event_id}/badges/{badge_id}/", json=data)
    print_response(response)

def get_badge(event_id, badge_id):
    """Recupera un badge specifico di un evento"""
    response = session.get(f"{BASE_URL}/events/{event_id}/badges/{badge_id}/")
    print_response(response)

def register_user_to_event(event_id, user_id):
    """Registra un utente a un evento"""
    response = session.post(f"{BASE_URL}/events/{event_id}/register-user/{user_id}/")
    print_response(response)

def get_user_from_event(event_id, user_id):
    """Recupera i dati di un utente registrato a un evento"""
    response = session.get(f"{BASE_URL}/events/{event_id}/users/{user_id}/")
    print_response(response)

def get_user_address(event_id, user_id):
    """Recupera l'address di un utente registrato a un evento"""
    response = session.get(f"{BASE_URL}/events/{event_id}/users/{user_id}/address/")
    print_response(response)

def get_event_addresses(event_id):
    """Recupera tutti gli address degli utenti iscritti a un evento"""
    response = session.get(f"{BASE_URL}/events/{event_id}/addresses/")
    print_response(response)


# ======== FUNZIONE PER STAMPARE LE RISPOSTE =========

def print_response(response):
    """Stampa il codice di stato e il JSON della risposta"""
    print(f"\nStatus Code: {response.status_code}")
    try:
        print("Response JSON:", response.json())
    except Exception:
        print("Response Text:", response.text)


# ======== ESECUZIONE DEI TEST =========

if __name__ == "__main__":
    # LOGIN
    if not login("goku", "Supersaiyan"):  # Cambia le credenziali
        exit()

    # TEST API
    print("\n🔹 TEST: Creazione di un evento 🔹")
    create_event()

    print("\n🔹 TEST: Recupero lista eventi 🔹")
    get_events()

    event_id = 1  # Modifica con un ID valido
    print(f"\n🔹 TEST: Aggiunta di un badge all'evento {event_id} 🔹")
    add_badge_to_event(event_id)

    badge_id = 1  # Modifica con un ID valido
    print(f"\n🔹 TEST: Modifica del badge {badge_id} nell'evento {event_id} 🔹")
    update_badge(event_id, badge_id)

    print(f"\n🔹 TEST: Recupero del badge {badge_id} dell'evento {event_id} 🔹")
    get_badge(event_id, badge_id)

    user_id = 1  # Modifica con un ID valido
    print(f"\n🔹 TEST: Registrazione dell'utente {user_id} all'evento {event_id} 🔹")
    register_user_to_event(event_id, user_id)

    print(f"\n🔹 TEST: Recupero dell'utente {user_id} all'evento {event_id} 🔹")
    get_user_from_event(event_id, user_id)

    print(f"\n🔹 TEST: Recupero dell'address dell'utente {user_id} all'evento {event_id} 🔹")
    get_user_address(event_id, user_id)

    print(f"\n🔹 TEST: Recupero di tutti gli address dell'evento {event_id} 🔹")
    get_event_addresses(event_id)

    # LOGOUT
    print("\n🔹 TEST: Logout 🔹")
    logout()
