# Supabase Client - Schnellstart

Ein vollständig modulares Python-System für Supabase-Datenbankoperationen.

## 🚀 Installation

```bash
# Dependencies installieren
pip install -r requirements_supabase.txt

# .env Datei erstellen
cp .env.example .env

# SUPABASE_URL und SUPABASE_KEY in .env eintragen
```

## 📁 Projektstruktur

```
supabase_client/           # Hauptmodul
├── client.py              # Supabase-Verbindung
├── config.py              # Konfiguration
├── services/              # Basis-Services
│   ├── base_service.py
│   └── crud_service.py    # CRUD-Operationen
├── models/                # Tabellen-spezifische Services
│   ├── users_service.py
│   └── example_service.py
└── utils/                 # Hilfsfunktionen

supabase_api.py            # ⭐ Hauptdatei - hier starten!
examples/                  # Beispiele
```

## 🎯 Verwendung in 3 Schritten

### 1. Basic - Beliebige Tabelle verwenden

```python
from supabase_api import SupabaseAPI

# API initialisieren
api = SupabaseAPI.from_env()

# Mit beliebiger Tabelle arbeiten
posts = api.table('posts')

# CRUD-Operationen
posts.create({'title': 'Neuer Post'})
posts.get_all(limit=10)
posts.find({'status': 'published'})
posts.update(123, {'title': 'Aktualisierter Titel'})
posts.delete(123)
```

### 2. Quick Methods - Noch einfacher

```python
# Ein-Zeiler für schnelle Operationen
api.quick_select('posts', filters={'status': 'published'})
api.quick_insert('posts', {'title': 'Test'})
api.quick_update('posts', 123, {'title': 'Neu'})
api.quick_delete('posts', 123)
```

### 3. Custom Services - Für häufig verwendete Tabellen

```python
# Built-in Users Service
api.users.get_by_email('user@example.com')
api.users.get_active_users(limit=10)
api.users.create_user(email='...', username='...')
```

## 📚 Vollständige CRUD-Operationen

```python
service = api.table('your_table')

# CREATE
service.create({'field': 'value'})
service.create_many([{...}, {...}])

# READ
service.get_all(limit=10, order_by='created_at')
service.get_by_id(123)
service.find({'status': 'active'}, limit=10)
service.find_one({'email': 'test@example.com'})
service.search('name', 'John', limit=5)

# UPDATE
service.update(123, {'field': 'new_value'})
service.update_many({'status': 'old'}, {'status': 'new'})

# DELETE
service.delete(123)
service.delete_many({'status': 'inactive'})

# UTILITIES
service.count()
service.count({'status': 'active'})
service.exists({'email': 'test@example.com'})
```

## 🔧 Eigene Services erstellen

Erstellen Sie `my_services/posts_service.py`:

```python
from supabase_client.services.crud_service import CRUDService

class PostsService(CRUDService):
    def __init__(self, client):
        super().__init__(client, "posts")

    def get_published(self, limit=10):
        return self.find(
            {'status': 'published'},
            order_by='published_at',
            ascending=False,
            limit=limit
        )

    def get_by_slug(self, slug):
        return self.find_one({'slug': slug})
```

Verwenden:

```python
from my_services.posts_service import PostsService

posts = api.custom_service(PostsService)
posts.get_published(limit=5)
posts.get_by_slug('my-post')
```

## 📝 Response-Format

Alle Methoden geben einheitliche Responses zurück:

```python
{
    "success": True,      # Erfolg oder Fehler
    "data": [...],        # Die Daten
    "count": 10,          # Anzahl (optional)
    "error": "...",       # Fehlermeldung (bei Fehler)
    "exists": True        # Boolean (bei exists())
}

# Verwendung
result = service.get_all()
if result['success']:
    for item in result['data']:
        print(item)
else:
    print(f"Fehler: {result['error']}")
```

## 🎓 Beispiele ausführen

```bash
# Basic usage
python examples/basic_usage.py

# Custom services
python examples/custom_service_example.py
```

## 🔑 Key Features

### ✅ Modular & Wiederverwendbar
Jede Komponente kann separat verwendet werden.

### ✅ Type-Safe Responses
Einheitliches Response-Format für alle Operationen.

### ✅ Fehlerbehandlung
Automatische Fehlerbehandlung mit klaren Fehlermeldungen.

### ✅ Erweiterbar
Einfach eigene Services für spezifische Tabellen erstellen.

### ✅ Vollständig dokumentiert
Jede Methode hat Docstrings und Beispiele.

## 🌟 Häufige Anwendungsfälle

### User Management

```python
# Neuen User erstellen
api.users.create_user(
    email='user@example.com',
    username='newuser'
)

# Email-Existenz prüfen
if api.users.email_exists('user@example.com')['exists']:
    print("Email bereits registriert")

# User suchen
user = api.users.get_by_email('user@example.com')
```

### Content Management

```python
posts = api.table('posts')

# Veröffentlichte Posts
posts.find({'status': 'published'}, order_by='date', limit=10)

# Post veröffentlichen
posts.update(post_id, {'status': 'published', 'published_at': 'now()'})

# Posts durchsuchen
posts.search('title', 'Python', limit=5)
```

### Bulk Operations

```python
# Mehrere erstellen
posts.create_many([
    {'title': 'Post 1', 'content': '...'},
    {'title': 'Post 2', 'content': '...'}
])

# Mehrere aktualisieren
posts.update_many(
    {'status': 'draft'},
    {'status': 'published'}
)
```

## 🐛 Troubleshooting

**"SUPABASE_URL ist nicht gesetzt"**
```python
from dotenv import load_dotenv
load_dotenv()  # .env Datei laden
```

**"Connection failed"**
- Prüfen Sie SUPABASE_URL und SUPABASE_KEY
- Testen Sie: `api.test_connection()`

**"Table not found"**
- Stellen Sie sicher, dass die Tabelle in Supabase existiert
- Prüfen Sie Row Level Security (RLS) Policies

## 📖 Weitere Dokumentation

- Vollständige Dokumentation: [supabase_client/README.md](supabase_client/README.md)
- Beispiele: [examples/](examples/)

## 💡 Tipps

1. **Services wiederverwenden**: Erstellen Sie Services einmal, verwenden Sie sie mehrfach
2. **Fehler behandeln**: Prüfen Sie immer `result['success']`
3. **Pagination nutzen**: Verwenden Sie `limit` bei großen Datenmengen
4. **Custom Services**: Erstellen Sie eigene Services für häufig genutzte Tabellen
5. **Umgebungsvariablen**: Speichern Sie niemals Credentials im Code

## 🚀 Los geht's!

```python
from supabase_api import SupabaseAPI

api = SupabaseAPI.from_env()

# Test connection
if api.test_connection():
    print("✅ Verbunden mit Supabase!")

    # Start using it
    result = api.table('your_table').get_all(limit=10)
    print(result['data'])
```

Viel Erfolg! 🎉
