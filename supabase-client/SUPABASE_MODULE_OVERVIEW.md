# Supabase Python Module - Komplette Übersicht

## 📦 Was wurde erstellt?

Ein vollständig modulares, wiederverwendbares Python-System für Supabase-Datenbankoperationen mit:

- ✅ Vollständige CRUD-Operationen
- ✅ Modulare, erweiterbare Architektur
- ✅ Tabellen-spezifische Services
- ✅ Typisierte Responses
- ✅ Umfassende Fehlerbehandlung
- ✅ Vollständige Dokumentation
- ✅ Beispiele für alle Funktionen

## 📁 Dateistruktur

```
Projekt/
│
├── supabase_client/                    # Hauptmodul
│   ├── __init__.py                     # Exports
│   ├── client.py                       # Supabase Client
│   ├── config.py                       # Konfigurationsmanagement
│   │
│   ├── services/                       # Service Layer
│   │   ├── __init__.py
│   │   ├── base_service.py            # Basis für alle Services
│   │   └── crud_service.py            # CRUD-Operationen
│   │
│   ├── models/                         # Tabellen-spezifische Services
│   │   ├── __init__.py
│   │   ├── users_service.py           # Users-Service (Beispiel)
│   │   └── example_service.py         # Template für neue Services
│   │
│   ├── utils/                          # Hilfsfunktionen
│   │   ├── __init__.py
│   │   └── helpers.py                 # Helper-Funktionen
│   │
│   └── README.md                       # Vollständige Dokumentation
│
├── supabase_api.py                     # ⭐ HAUPT-API DATEI
│
├── examples/                           # Beispiele
│   ├── basic_usage.py                 # Basis-Operationen
│   └── custom_service_example.py      # Custom Services
│
├── requirements_supabase.txt           # Dependencies
├── .env.example                        # Environment Template
├── SUPABASE_QUICKSTART.md             # Schnellstart-Guide
└── SUPABASE_MODULE_OVERVIEW.md        # Diese Datei
```

## 🎯 Haupt-Einstiegspunkt

### `supabase_api.py`

Dies ist die Hauptdatei, die Sie verwenden sollten:

```python
from supabase_api import SupabaseAPI

# API initialisieren
api = SupabaseAPI.from_env()

# Mit beliebiger Tabelle arbeiten
users = api.table('users')
users.get_all()
users.create({...})
users.find({...})

# Oder Quick Methods
api.quick_select('table', filters={...})
api.quick_insert('table', data={...})
```

## 🧩 Module im Detail

### 1. **supabase_client/client.py**
- `SupabaseClient`: Verwaltet Verbindung zu Supabase
- Methoden: `from_env()`, `from_dict()`, `table()`, `test_connection()`

### 2. **supabase_client/config.py**
- `SupabaseConfig`: Konfigurationsmanagement
- Liest aus Umgebungsvariablen oder Dictionary

### 3. **supabase_client/services/base_service.py**
- `BaseService`: Basisklasse für alle Services
- Gemeinsame Funktionalität und Response-Handling

### 4. **supabase_client/services/crud_service.py**
- `CRUDService`: Vollständige CRUD-Operationen
- **Create:** `create()`, `create_many()`
- **Read:** `get_all()`, `get_by_id()`, `find()`, `find_one()`, `search()`
- **Update:** `update()`, `update_many()`
- **Delete:** `delete()`, `delete_many()`
- **Utils:** `count()`, `exists()`

### 5. **supabase_client/models/users_service.py**
- `UsersService`: Beispiel für tabellen-spezifischen Service
- Custom Methods: `get_by_email()`, `get_active_users()`, `create_user()`, etc.

### 6. **supabase_client/models/example_service.py**
- Template für eigene Services
- Kopieren und anpassen für Ihre Tabellen

### 7. **supabase_client/utils/helpers.py**
- Helper-Funktionen: `format_response()`, `handle_pagination()`, etc.

## 🚀 Verwendungsbeispiele

### Minimal Example

```python
from supabase_api import SupabaseAPI

api = SupabaseAPI.from_env()
users = api.table('users')

# Create
result = users.create({'name': 'John', 'email': 'john@example.com'})

# Read
result = users.get_all(limit=10)

# Find
result = users.find({'email': 'john@example.com'})

# Update
result = users.update(123, {'name': 'Jane'})

# Delete
result = users.delete(123)
```

### Custom Service Example

```python
# 1. Eigenen Service erstellen
from supabase_client.services.crud_service import CRUDService

class PostsService(CRUDService):
    def __init__(self, client):
        super().__init__(client, "posts")

    def get_published(self):
        return self.find({'status': 'published'})

# 2. Verwenden
api = SupabaseAPI.from_env()
posts = api.custom_service(PostsService)
result = posts.get_published()
```

## 📊 Response-Format

Alle Methoden geben ein standardisiertes Dictionary zurück:

```python
{
    "success": True,           # Boolean: Erfolg/Fehler
    "data": [...] or {...},    # Die tatsächlichen Daten
    "count": 10,               # Optional: Anzahl
    "error": "message",        # Optional: Fehlermeldung
    "exists": True             # Optional: Existenz-Check
}
```

## 🔧 Setup

### 1. Dependencies installieren

```bash
pip install -r requirements_supabase.txt
```

### 2. Umgebungsvariablen setzen

```bash
# .env erstellen
cp .env.example .env

# Eintragen:
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-or-service-key
```

### 3. Verwenden

```python
from dotenv import load_dotenv
load_dotenv()

from supabase_api import SupabaseAPI
api = SupabaseAPI.from_env()
```

## 📚 Verfügbare Methoden

### CRUDService Methoden

| Methode | Beschreibung | Beispiel |
|---------|-------------|----------|
| `create(data)` | Erstellt einen Datensatz | `service.create({'name': 'John'})` |
| `create_many(data)` | Erstellt mehrere Datensätze | `service.create_many([{...}, {...}])` |
| `get_all(limit, offset, order_by)` | Holt alle Datensätze | `service.get_all(limit=10)` |
| `get_by_id(id_value)` | Holt Datensatz nach ID | `service.get_by_id(123)` |
| `find(filters, limit)` | Sucht mit Filtern | `service.find({'status': 'active'})` |
| `find_one(filters)` | Findet einen Datensatz | `service.find_one({'email': 'x@y.z'})` |
| `search(column, term)` | Textsuche | `service.search('name', 'John')` |
| `update(id, data)` | Aktualisiert nach ID | `service.update(123, {'name': 'New'})` |
| `update_many(filters, data)` | Aktualisiert mehrere | `service.update_many({...}, {...})` |
| `delete(id)` | Löscht nach ID | `service.delete(123)` |
| `delete_many(filters)` | Löscht mehrere | `service.delete_many({'status': 'old'})` |
| `count(filters)` | Zählt Datensätze | `service.count()` |
| `exists(filters)` | Prüft Existenz | `service.exists({'email': 'x@y.z'})` |

### SupabaseAPI Quick Methods

| Methode | Beschreibung | Beispiel |
|---------|-------------|----------|
| `quick_select(table, filters)` | Schnelles SELECT | `api.quick_select('users', {...})` |
| `quick_insert(table, data)` | Schnelles INSERT | `api.quick_insert('users', {...})` |
| `quick_update(table, id, data)` | Schnelles UPDATE | `api.quick_update('users', 1, {...})` |
| `quick_delete(table, id)` | Schnelles DELETE | `api.quick_delete('users', 1)` |

## 🎓 Lernressourcen

1. **Schnellstart**: [SUPABASE_QUICKSTART.md](SUPABASE_QUICKSTART.md)
2. **Vollständige Docs**: [supabase_client/README.md](supabase_client/README.md)
3. **Beispiele**: [examples/](examples/)
   - `basic_usage.py` - Basis-CRUD-Operationen
   - `custom_service_example.py` - Custom Services

## 🔄 Workflow für neue Tabellen

### 1. Quick & Simple (Empfohlen für Start)

```python
# Verwenden Sie einfach api.table() ohne eigenen Service
posts = api.table('posts')
posts.get_all()
posts.create({...})
```

### 2. Custom Service (Für häufig genutzte Tabellen)

```python
# 1. Kopieren Sie example_service.py
# 2. Umbenennen zu posts_service.py
# 3. Anpassen der Tabelle und Methoden
# 4. Importieren und verwenden

from my_services.posts_service import PostsService
posts = api.custom_service(PostsService)
```

## 🌟 Best Practices

1. **Umgebungsvariablen**: Niemals Credentials im Code
2. **Service-Wiederverwendung**: Services einmal erstellen, mehrfach nutzen
3. **Error Handling**: Immer `result['success']` prüfen
4. **Pagination**: Bei großen Datenmengen `limit` verwenden
5. **Custom Services**: Für häufig genutzte Tabellen eigene Services erstellen

## 🐛 Debugging

### Connection testen

```python
if api.test_connection():
    print("✅ Verbunden!")
else:
    print("❌ Fehler bei Verbindung")
```

### Responses prüfen

```python
result = users.get_all()

if result['success']:
    print(f"Daten: {result['data']}")
else:
    print(f"Fehler: {result['error']}")
```

## 📦 Dependencies

- `supabase` - Supabase Python Client
- `python-dotenv` - Environment Variables
- `pydantic` - (Optional) Data Validation

## 🚀 Nächste Schritte

1. Dependencies installieren: `pip install -r requirements_supabase.txt`
2. `.env` konfigurieren
3. Beispiele ausführen: `python examples/basic_usage.py`
4. Mit Ihren Tabellen experimentieren
5. Eigene Services erstellen nach Bedarf

## 💡 Tipps

- Starten Sie mit `api.table()` für schnelle Tests
- Erstellen Sie Custom Services für komplexe Operationen
- Nutzen Sie die Quick Methods für Ein-Zeiler
- Lesen Sie die Beispiele für Inspiration

## 🎉 Fertig!

Sie haben jetzt ein vollständiges, produktionsreifes Supabase-Modul-System!

Viel Erfolg! 🚀
