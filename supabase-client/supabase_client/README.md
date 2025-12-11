# Supabase Client Module

Ein modulares, wiederverwendbares Python-Modul für Supabase-Datenbankoperationen.

## Features

- ✅ Vollständige CRUD-Operationen (Create, Read, Update, Delete)
- ✅ Modulare Architektur für Wiederverwendbarkeit
- ✅ Typisierte Responses
- ✅ Einfache Konfiguration über Umgebungsvariablen
- ✅ Tabellen-spezifische Services
- ✅ Such- und Filterfunktionen
- ✅ Pagination-Unterstützung
- ✅ Fehlerbehandlung
- ✅ Vollständig dokumentiert

## Installation

### Abhängigkeiten installieren:

```bash
pip install supabase python-dotenv
```

### Umgebungsvariablen setzen:

Erstellen Sie eine `.env` Datei:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-or-service-key
```

## Schnellstart

### 1. Einfache Verwendung

```python
from supabase_api import SupabaseAPI

# API initialisieren
api = SupabaseAPI.from_env()

# Mit beliebiger Tabelle arbeiten
users = api.table('users')

# Alle Benutzer abrufen
result = users.get_all(limit=10)
print(result['data'])

# Benutzer erstellen
result = users.create({
    'name': 'John Doe',
    'email': 'john@example.com'
})

# Benutzer suchen
result = users.find({'email': 'john@example.com'})

# Benutzer aktualisieren
result = users.update(123, {'name': 'Jane Doe'})

# Benutzer löschen
result = users.delete(123)
```

### 2. Mit spezifischen Services

```python
from supabase_api import SupabaseAPI

api = SupabaseAPI.from_env()

# Users Service verwenden (hat zusätzliche Methoden)
result = api.users.get_by_email('user@example.com')
result = api.users.get_active_users(limit=10)
result = api.users.search_users('john', limit=5)
```

### 3. Quick Methods

```python
# Schnelle Operationen ohne Service erstellen
api.quick_select('posts', filters={'status': 'published'}, limit=10)
api.quick_insert('posts', {'title': 'New Post', 'content': '...'})
api.quick_update('posts', 123, {'title': 'Updated Title'})
api.quick_delete('posts', 123)
```

## Modul-Struktur

```
supabase_client/
├── __init__.py              # Haupt-Exports
├── client.py                # Supabase Client
├── config.py                # Konfiguration
├── services/
│   ├── __init__.py
│   ├── base_service.py      # Basis-Service
│   └── crud_service.py      # CRUD-Operationen
├── models/
│   ├── __init__.py
│   ├── users_service.py     # Users-spezifischer Service
│   └── example_service.py   # Template für eigene Services
└── utils/
    ├── __init__.py
    └── helpers.py           # Hilfsfunktionen

supabase_api.py              # Haupt-API (verwenden Sie diese!)
```

## Detaillierte Verwendung

### CRUD-Operationen

#### Create (Erstellen)

```python
# Einzelnen Datensatz erstellen
result = users.create({
    'name': 'John Doe',
    'email': 'john@example.com',
    'age': 30
})

# Mehrere Datensätze erstellen
result = users.create_many([
    {'name': 'John', 'email': 'john@example.com'},
    {'name': 'Jane', 'email': 'jane@example.com'}
])
```

#### Read (Lesen)

```python
# Alle Datensätze
result = users.get_all(limit=10, order_by='created_at')

# Nach ID
result = users.get_by_id(123)

# Mit Filtern suchen
result = users.find({
    'status': 'active',
    'role': 'admin'
}, limit=10)

# Einzelnen Datensatz finden
result = users.find_one({'email': 'john@example.com'})

# Textsuche
result = users.search('name', 'John', limit=10)

# Zählen
result = users.count()
result = users.count({'status': 'active'})

# Existenz prüfen
result = users.exists({'email': 'john@example.com'})
```

#### Update (Aktualisieren)

```python
# Einzelnen Datensatz aktualisieren
result = users.update(123, {
    'name': 'Jane Doe',
    'email': 'jane@example.com'
})

# Mehrere Datensätze aktualisieren
result = users.update_many(
    {'status': 'pending'},
    {'status': 'active'}
)
```

#### Delete (Löschen)

```python
# Einzelnen Datensatz löschen
result = users.delete(123)

# Mehrere Datensätze löschen
result = users.delete_many({'status': 'inactive'})
```

### Eigene Services erstellen

Erstellen Sie eigene tabellen-spezifische Services:

```python
# my_services/posts_service.py
from supabase_client.services.crud_service import CRUDService
from supabase_client import SupabaseClient

class PostsService(CRUDService):
    def __init__(self, client: SupabaseClient):
        super().__init__(client, "posts")

    def get_published_posts(self, limit=10):
        return self.find(
            {'status': 'published'},
            limit=limit,
            order_by='published_at',
            ascending=False
        )

    def get_by_slug(self, slug):
        return self.find_one({'slug': slug})

    def publish_post(self, post_id):
        return self.update(post_id, {
            'status': 'published',
            'published_at': 'now()'
        })
```

Verwenden:

```python
from supabase_api import SupabaseAPI
from my_services.posts_service import PostsService

api = SupabaseAPI.from_env()
posts = api.custom_service(PostsService)

result = posts.get_published_posts(limit=5)
result = posts.get_by_slug('my-first-post')
result = posts.publish_post(123)
```

### Response-Format

Alle Methoden geben ein standardisiertes Response-Dictionary zurück:

```python
{
    "success": True,        # Boolean: Erfolg oder Fehler
    "data": [...],          # Die tatsächlichen Daten
    "count": 10,            # Anzahl (bei count-Operationen)
    "error": "...",         # Fehlermeldung (bei Fehler)
    "exists": True          # Boolean (bei exists-Operationen)
}
```

### Fehlerbehandlung

```python
result = users.create({'name': 'John'})

if result['success']:
    print("Erfolg!", result['data'])
else:
    print("Fehler:", result['error'])
```

### Erweiterte Queries

Für komplexere Queries können Sie direkt auf die Table zugreifen:

```python
# Direkter Zugriff auf Supabase Table
table = api.client.table('users')

result = (
    table
    .select('id, name, email')
    .eq('status', 'active')
    .gt('age', 18)
    .order('created_at', desc=True)
    .limit(10)
    .execute()
)
```

## Beispiele

### Beispiel 1: User Management

```python
from supabase_api import SupabaseAPI

api = SupabaseAPI.from_env()

# Neuen User erstellen
result = api.users.create_user(
    email='new@example.com',
    username='newuser',
    first_name='New',
    last_name='User'
)

# Prüfen ob Email existiert
result = api.users.email_exists('new@example.com')
if result['exists']:
    print("Email bereits registriert!")

# User nach Email suchen
result = api.users.get_by_email('new@example.com')
user = result['data']

# User aktualisieren
if user:
    api.users.update(user['id'], {'status': 'verified'})

# Aktive Users abrufen
result = api.users.get_active_users(limit=10)
```

### Beispiel 2: Blog Posts

```python
# Posts-Tabelle verwenden
posts = api.table('posts')

# Neuen Post erstellen
result = posts.create({
    'title': 'Mein erster Post',
    'content': 'Das ist der Inhalt...',
    'author_id': 123,
    'status': 'draft'
})

# Veröffentlichte Posts abrufen
result = posts.find(
    {'status': 'published'},
    order_by='published_at',
    ascending=False,
    limit=10
)

# Posts durchsuchen
result = posts.search('title', 'Python', limit=5)
```

### Beispiel 3: Bulk Operations

```python
# Mehrere Datensätze erstellen
users = api.table('users')
result = users.create_many([
    {'name': 'User 1', 'email': 'user1@example.com'},
    {'name': 'User 2', 'email': 'user2@example.com'},
    {'name': 'User 3', 'email': 'user3@example.com'},
])

# Mehrere Datensätze aktualisieren
result = users.update_many(
    {'status': 'pending'},
    {'status': 'active', 'activated_at': 'now()'}
)

# Mehrere Datensätze löschen
result = users.delete_many({'status': 'inactive'})
```

## Testing

```python
from supabase_api import SupabaseAPI

# Connection testen
api = SupabaseAPI.from_env()

if api.test_connection():
    print("✅ Verbindung zu Supabase erfolgreich!")
else:
    print("❌ Verbindung fehlgeschlagen")
```

## Best Practices

1. **Umgebungsvariablen verwenden**: Speichern Sie niemals Credentials im Code
2. **Services wiederverwenden**: Erstellen Sie Service-Instanzen einmal und verwenden Sie sie wieder
3. **Fehler behandeln**: Prüfen Sie immer `result['success']` vor dem Zugriff auf Daten
4. **Spezifische Services erstellen**: Für häufig verwendete Tabellen eigene Services schreiben
5. **Pagination verwenden**: Bei großen Datenmengen immer `limit` setzen

## Troubleshooting

### "SUPABASE_URL ist nicht gesetzt"

Stellen Sie sicher, dass die `.env` Datei existiert und geladen wird:

```python
from dotenv import load_dotenv
load_dotenv()

from supabase_api import SupabaseAPI
api = SupabaseAPI.from_env()
```

### "Connection test failed"

- Überprüfen Sie Ihre SUPABASE_URL
- Überprüfen Sie Ihren SUPABASE_KEY
- Stellen Sie sicher, dass Sie Internetzugang haben
- Prüfen Sie, ob Ihr Supabase-Projekt aktiv ist

## Lizenz

MIT License - Frei verwendbar für alle Projekte!
