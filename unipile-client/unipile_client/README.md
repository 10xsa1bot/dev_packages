# Unipile Client Module

Ein modulares Python-Modul für Unipile API-Operationen.

## Features

- ✅ LinkedIn Profile abrufen (eigenes & andere)
- ✅ Modulare Architektur
- ✅ Typisierte Responses
- ✅ Einfache Konfiguration über Umgebungsvariablen
- ✅ Fehlerbehandlung
- ✅ Vollständig dokumentiert

## Installation

### Abhängigkeiten installieren:

```bash
pip install requests python-dotenv
```

### Umgebungsvariablen setzen:

Fügen Sie zu Ihrer `.env` Datei hinzu:

```env
UNIPILE_DSN=your-unipile-dsn
UNIPILE_API_URL=https://api4.unipile.com:13443  # Optional
```

## Schnellstart

### 1. Einfache Verwendung

```python
from unipile_api import UnipileAPI

# API initialisieren
api = UnipileAPI.from_env()

# Eigenes Profil abrufen
result = api.profiles.get_own_profile(account_id="your_account_id")

if result['success']:
    profile = result['data']
    print(f"Name: {profile.get('name')}")
    print(f"Headline: {profile.get('headline')}")
    print(f"Connections: {profile.get('connections')}")
else:
    print(f"Fehler: {result['error']}")
```

### 2. Fremdes Profil abrufen

```python
# Nach LinkedIn URL
result = api.profiles.get_user_profile(
    account_id="your_account_id",
    identifier="https://linkedin.com/in/johndoe"
)

# Nach Username
result = api.profiles.get_user_profile(
    account_id="your_account_id",
    identifier="johndoe"
)

if result['success']:
    profile = result['data']
    print(f"Name: {profile.get('name')}")
    print(f"Location: {profile.get('location')}")
    print(f"About: {profile.get('about')}")
```

## Modul-Struktur

```
unipile_client/
├── __init__.py              # Haupt-Exports
├── client.py                # Unipile Client
├── config.py                # Konfiguration
├── profiles.py              # Profile-Service
└── README.md                # Diese Datei

unipile_api.py               # Haupt-API (verwenden Sie diese!)
```

## Verfügbare Methoden

### ProfilesService

#### get_own_profile(account_id, provider="LINKEDIN")

Holt das eigene Profil (Account-Besitzer-Profil).

**Parameter:**
- `account_id` (str): Ihre Unipile Account ID
- `provider` (str): Provider (default: "LINKEDIN")

**Returns:**
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
        ...
    },
    "message": "Request successful"
}
```

**Beispiel:**
```python
result = api.profiles.get_own_profile(account_id="acc_123")
if result['success']:
    profile = result['data']
    print(f"Mein Name: {profile['name']}")
```

#### get_user_profile(account_id, identifier, provider="LINKEDIN")

Holt das Profil eines anderen LinkedIn-Users.

**Parameter:**
- `account_id` (str): Ihre Unipile Account ID
- `identifier` (str): LinkedIn URL, Username oder Member ID
  - "https://linkedin.com/in/username"
  - "username"
  - LinkedIn Member ID
- `provider` (str): Provider (default: "LINKEDIN")

**Returns:**
```python
{
    "success": True,
    "data": {
        "id": "profile_id",
        "name": "User Name",
        "headline": "Professional Title",
        "location": "City, Country",
        "profile_url": "https://linkedin.com/in/...",
        "about": "About section text",
        "experience": [...],
        "education": [...],
        "connections": 500,
        ...
    },
    "message": "Request successful"
}
```

**Beispiel:**
```python
# Mit URL
result = api.profiles.get_user_profile(
    account_id="acc_123",
    identifier="https://linkedin.com/in/johndoe"
)

# Mit Username
result = api.profiles.get_user_profile(
    account_id="acc_123",
    identifier="johndoe"
)
```

#### Convenience Methods

**get_user_profile_by_url(account_id, profile_url, provider="LINKEDIN")**

Wrapper speziell für Profile-URLs.

```python
result = api.profiles.get_user_profile_by_url(
    account_id="acc_123",
    profile_url="https://www.linkedin.com/in/johndoe/"
)
```

**get_user_profile_by_username(account_id, username, provider="LINKEDIN")**

Wrapper speziell für Usernames.

```python
result = api.profiles.get_user_profile_by_username(
    account_id="acc_123",
    username="johndoe"
)
```

**extract_profile_data(result)**

Extrahiert saubere Profildaten aus API-Response.

```python
result = api.profiles.get_own_profile(account_id="acc_123")
profile = api.profiles.extract_profile_data(result)
if profile:
    print(profile['name'])
```

**compare_profiles(account_id, identifier1, identifier2, provider="LINKEDIN")**

Vergleicht zwei Profile.

```python
result = api.profiles.compare_profiles(
    account_id="acc_123",
    identifier1="johndoe",
    identifier2="janedoe"
)

if result['success']:
    profile1 = result['profile1']
    profile2 = result['profile2']
    print(f"{profile1['name']} vs {profile2['name']}")
```

## Response-Format

Alle Methoden geben ein standardisiertes Response-Dictionary zurück:

```python
{
    "success": True,           # Boolean: Erfolg oder Fehler
    "data": {...},             # Die tatsächlichen Daten
    "status_code": 200,        # HTTP Status Code
    "message": "...",          # Nachricht
    "error": "...",            # Fehlermeldung (bei Fehler)
    "error_detail": {...},     # Detaillierte Fehlerinfo (bei Fehler)
    "context": "..."           # Kontext (bei Fehler)
}
```

## Fehlerbehandlung

```python
result = api.profiles.get_user_profile(
    account_id="acc_123",
    identifier="johndoe"
)

if result['success']:
    profile = result['data']
    print(f"Erfolgreich: {profile['name']}")
else:
    print(f"Fehler: {result['error']}")
    if 'error_detail' in result:
        print(f"Details: {result['error_detail']}")
```

## Beispiele

### Beispiel 1: Eigenes Profil abrufen

```python
from unipile_api import UnipileAPI

api = UnipileAPI.from_env()

result = api.profiles.get_own_profile(account_id="acc_123")

if result['success']:
    profile = result['data']
    print(f"Name: {profile.get('name')}")
    print(f"Headline: {profile.get('headline')}")
    print(f"Location: {profile.get('location')}")
    print(f"Connections: {profile.get('connections')}")
    print(f"Profile URL: {profile.get('profile_url')}")
```

### Beispiel 2: Fremdes Profil nach URL abrufen

```python
result = api.profiles.get_user_profile_by_url(
    account_id="acc_123",
    profile_url="https://www.linkedin.com/in/johndoe/"
)

if result['success']:
    profile = result['data']
    print(f"\nProfile von: {profile.get('name')}")
    print(f"Headline: {profile.get('headline')}")
    print(f"About: {profile.get('about', 'Keine Info')[:100]}...")

    # Experience
    if profile.get('experience'):
        print(f"\nErfahrung:")
        for exp in profile['experience'][:3]:  # Erste 3
            print(f"  - {exp.get('title')} at {exp.get('company')}")
```

### Beispiel 3: Mehrere Profile abrufen

```python
usernames = ['johndoe', 'janedoe', 'bobsmith']
account_id = "acc_123"

for username in usernames:
    result = api.profiles.get_user_profile_by_username(
        account_id=account_id,
        username=username
    )

    if result['success']:
        profile = result['data']
        print(f"{profile.get('name')} - {profile.get('headline')}")
    else:
        print(f"Fehler bei {username}: {result['error']}")
```

### Beispiel 4: Profile vergleichen

```python
result = api.profiles.compare_profiles(
    account_id="acc_123",
    identifier1="johndoe",
    identifier2="janedoe"
)

if result['success']:
    p1 = result['profile1']
    p2 = result['profile2']

    print(f"Vergleich:")
    print(f"{p1['name']} ({p1.get('connections', 0)} connections)")
    print(f"  vs")
    print(f"{p2['name']} ({p2.get('connections', 0)} connections)")
```

## Configuration

### Von Umgebungsvariablen

```python
from unipile_api import UnipileAPI

api = UnipileAPI.from_env()
```

### Von Dictionary

```python
api = UnipileAPI.from_dict({
    'dsn': 'your-dsn',
    'api_url': 'https://api4.unipile.com:13443'
})
```

### Direkt

```python
api = UnipileAPI(dsn='your-dsn')
```

## Connection testen

```python
api = UnipileAPI.from_env()

if api.test_connection():
    print("✅ Verbindung zu Unipile erfolgreich!")
else:
    print("❌ Verbindung fehlgeschlagen")
```

## API-Referenzen

- **Get Own Profile**: https://developer.unipile.com/reference/userscontroller_getaccountownerprofile
- **Get User Profile**: https://developer.unipile.com/reference/userscontroller_getprofilebyidentifier

## Best Practices

1. **Umgebungsvariablen verwenden**: Speichern Sie niemals DSN im Code
2. **Fehlerbehandlung**: Prüfen Sie immer `result['success']`
3. **Rate Limiting beachten**: Unipile hat Rate Limits
4. **Account ID speichern**: Speichern Sie Ihre Account ID für wiederholte Verwendung

## Troubleshooting

### "UNIPILE_DSN ist nicht gesetzt"

```python
from dotenv import load_dotenv
load_dotenv()

from unipile_api import UnipileAPI
api = UnipileAPI.from_env()
```

### "Connection test failed"

- Überprüfen Sie Ihren UNIPILE_DSN
- Stellen Sie sicher, dass Sie Internetzugang haben
- Prüfen Sie die Unipile API Status

### "Profile not found"

- Überprüfen Sie den identifier
- Stellen Sie sicher, dass das Profil öffentlich ist
- Prüfen Sie, ob Ihre Account ID korrekt ist

## Lizenz

MIT License - Frei verwendbar für alle Projekte!
