# Unipile Client - Schnellstart

Ein modulares Python-System für Unipile API-Operationen (LinkedIn Profile abrufen).

## 🚀 Installation

```bash
# Dependencies installieren (falls noch nicht vorhanden)
pip install requests python-dotenv

# .env Datei erstellen/ergänzen
# Fügen Sie hinzu:
UNIPILE_DSN=your-unipile-dsn
```

## 📁 Projektstruktur

```
backend/
├── unipile_client/           # Hauptmodul
│   ├── client.py             # Unipile-Verbindung
│   ├── config.py             # Konfiguration
│   ├── profiles.py           # Profile-Service
│   └── README.md             # Vollständige Doku
│
├── unipile_api.py            # ⭐ Hauptdatei - hier starten!
└── unipile_examples/         # Beispiele
```

## 🎯 Verwendung in 3 Schritten

### 1. API initialisieren

```python
from unipile_api import UnipileAPI

# Von Umgebungsvariablen
api = UnipileAPI.from_env()

# Oder direkt
api = UnipileAPI(dsn="your-dsn")
```

### 2. Eigenes Profil abrufen

```python
result = api.profiles.get_own_profile(account_id="your_account_id")

if result['success']:
    profile = result['data']
    print(f"Name: {profile['name']}")
    print(f"Headline: {profile['headline']}")
    print(f"Connections: {profile.get('connections')}")
```

### 3. Fremdes Profil abrufen

```python
# Mit LinkedIn URL
result = api.profiles.get_user_profile(
    account_id="your_account_id",
    identifier="https://linkedin.com/in/username"
)

# Oder mit Username
result = api.profiles.get_user_profile(
    account_id="your_account_id",
    identifier="username"
)

if result['success']:
    profile = result['data']
    print(f"Name: {profile['name']}")
    print(f"Location: {profile.get('location')}")
```

## 📚 Verfügbare Methoden

### Eigenes Profil

```python
result = api.profiles.get_own_profile(
    account_id="acc_123"
)
```

### Fremdes Profil

```python
# Universal method
result = api.profiles.get_user_profile(
    account_id="acc_123",
    identifier="username_or_url"
)

# Convenience methods
result = api.profiles.get_user_profile_by_url(
    account_id="acc_123",
    profile_url="https://linkedin.com/in/username"
)

result = api.profiles.get_user_profile_by_username(
    account_id="acc_123",
    username="username"
)
```

### Profile vergleichen

```python
result = api.profiles.compare_profiles(
    account_id="acc_123",
    identifier1="user1",
    identifier2="user2"
)

if result['success']:
    profile1 = result['profile1']
    profile2 = result['profile2']
```

## 📝 Response-Format

```python
{
    "success": True,
    "data": {
        "id": "profile_id",
        "name": "User Name",
        "headline": "Professional Title",
        "location": "City, Country",
        "profile_url": "https://linkedin.com/in/...",
        "profile_picture": "https://...",
        "connections": 500,
        "followers": 1000,
        "about": "About text...",
        "experience": [...],
        "education": [...],
        ...
    },
    "message": "Request successful"
}
```

## 🔑 Setup

### 1. DSN erhalten

1. Gehen Sie zu Unipile Dashboard
2. Erstellen Sie einen Account/Integration
3. Kopieren Sie den DSN

### 2. Environment Variable setzen

```bash
# In .env
UNIPILE_DSN=your-dsn-here
```

### 3. Verwenden

```python
from dotenv import load_dotenv
load_dotenv()

from unipile_api import UnipileAPI
api = UnipileAPI.from_env()
```

## 🎓 Beispiel ausführen

```bash
cd backend/unipile_examples
python basic_usage.py
```

## 🔧 Häufige Anwendungsfälle

### User-Info sammeln

```python
def get_user_info(account_id, username):
    api = UnipileAPI.from_env()

    result = api.profiles.get_user_profile(
        account_id=account_id,
        identifier=username
    )

    if result['success']:
        profile = result['data']
        return {
            'name': profile.get('name'),
            'headline': profile.get('headline'),
            'location': profile.get('location'),
            'connections': profile.get('connections'),
            'url': profile.get('profile_url')
        }
    return None
```

### Batch Profile abrufen

```python
def get_multiple_profiles(account_id, usernames):
    api = UnipileAPI.from_env()
    profiles = []

    for username in usernames:
        result = api.profiles.get_user_profile_by_username(
            account_id=account_id,
            username=username
        )

        if result['success']:
            profiles.append(result['data'])

    return profiles

# Verwendung
usernames = ['user1', 'user2', 'user3']
profiles = get_multiple_profiles('acc_123', usernames)
```

## 🐛 Troubleshooting

**"UNIPILE_DSN ist nicht gesetzt"**
```bash
# Prüfen Sie .env
cat .env | grep UNIPILE_DSN

# Stellen Sie sicher, dass load_dotenv() aufgerufen wird
from dotenv import load_dotenv
load_dotenv()
```

**"Connection failed"**
- Prüfen Sie Ihren DSN
- Testen Sie: `api.test_connection()`
- Überprüfen Sie Internetverbindung

**"Profile not found"**
- Stellen Sie sicher, dass der Username/URL korrekt ist
- Profil muss öffentlich sein
- Account ID muss korrekt sein

## 📖 API-Referenzen

- **Get Own Profile**: https://developer.unipile.com/reference/userscontroller_getaccountownerprofile
- **Get User Profile**: https://developer.unipile.com/reference/userscontroller_getprofilebyidentifier

## 💡 Tipps

1. **Account ID**: Ihre Unipile Account ID finden Sie im Unipile Dashboard
2. **Rate Limiting**: Beachten Sie Unipile's Rate Limits
3. **Fehlerbehandlung**: Prüfen Sie immer `result['success']`
4. **Identifier**: Funktioniert mit URL, Username oder Member ID

## 🚀 Los geht's!

```python
from unipile_api import UnipileAPI

api = UnipileAPI.from_env()

# Test connection
if api.test_connection():
    print("✅ Verbunden mit Unipile!")

    # Get own profile
    result = api.profiles.get_own_profile(account_id="your_account_id")
    if result['success']:
        print(f"Hallo {result['data']['name']}!")
```

Viel Erfolg! 🎉
