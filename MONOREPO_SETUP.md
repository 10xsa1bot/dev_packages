# Monorepo Setup Guide

Dieses Projekt verwendet ein Monorepo mit wiederverwendbaren Packages in `dev_packages/`.

## 📦 Struktur

```
linkedin_social_selling/
│
├── backend/                      # Haupt-Backend-Anwendung
│   ├── fastapi.py
│   ├── requirements.txt
│   ├── install_packages.sh      # Package-Installation (Linux/Mac)
│   └── install_packages.bat     # Package-Installation (Windows)
│
├── dev_packages/                 # Wiederverwendbare Packages
│   ├── README.md                # Monorepo-Dokumentation
│   │
│   ├── supabase-client/         # Supabase Package
│   │   ├── supabase_client/
│   │   ├── supabase_api.py
│   │   ├── setup.py
│   │   ├── pyproject.toml
│   │   └── README.md
│   │
│   └── unipile-client/          # Unipile Package
│       ├── unipile_client/
│       ├── unipile_api.py
│       ├── setup.py
│       ├── pyproject.toml
│       └── README.md
│
└── src/                          # Frontend (React)
```

## 🚀 Setup für dieses Projekt

### 1. Backend Dependencies installieren

```bash
cd backend
pip install -r requirements.txt
```

### 2. Dev Packages installieren

**Linux/Mac:**
```bash
cd backend
chmod +x install_packages.sh
./install_packages.sh
```

**Windows:**
```bash
cd backend
install_packages.bat
```

**Oder manuell:**
```bash
# Von der Projekt-Root
pip install -e dev_packages/supabase-client
pip install -e dev_packages/unipile-client
```

### 3. Umgebungsvariablen setzen

```bash
# In backend/.env
API_TOKEN=your-token
SUPABASE_URL=your-url
SUPABASE_KEY=your-key
UNIPILE_DSN=your-dsn
```

### 4. Verwenden

```python
from supabase_api import SupabaseAPI
from unipile_api import UnipileAPI

supabase = SupabaseAPI.from_env()
unipile = UnipileAPI.from_env()
```

## 🔧 Packages in anderen Projekten verwenden

### Option 1: Via Git (Empfohlen)

```bash
# In einem anderen Projekt
pip install git+https://github.com/yourusername/linkedin_social_selling.git#subdirectory=dev_packages/supabase-client
pip install git+https://github.com/yourusername/linkedin_social_selling.git#subdirectory=dev_packages/unipile-client
```

### Option 2: Lokaler Pfad

```bash
# Wenn Sie das Repo gecloned haben
pip install -e /path/to/linkedin_social_selling/dev_packages/supabase-client
pip install -e /path/to/linkedin_social_selling/dev_packages/unipile-client
```

### Option 3: Bauen und Installieren

```bash
# Package builden
cd dev_packages/supabase-client
python -m build

# In anderem Projekt installieren
pip install /path/to/linkedin_social_selling/dev_packages/supabase-client/dist/supabase_client-1.0.0-py3-none-any.whl
```

## 📝 Development Workflow

### Package-Code ändern

```bash
# Packages im editable mode installieren
pip install -e dev_packages/supabase-client
pip install -e dev_packages/unipile-client

# Änderungen am Code in dev_packages/*/
# sind sofort verfügbar, ohne Neuinstallation!
```

### Neues Feature hinzufügen

1. Code in `dev_packages/supabase-client/supabase_client/` ändern
2. Tests schreiben (optional)
3. Änderungen testen im Backend
4. Committen

### Version erhöhen

Bei Breaking Changes oder neuen Features:

1. Version in `setup.py` erhöhen
2. Version in `pyproject.toml` erhöhen
3. Version in `__init__.py` erhöhen
4. CHANGELOG erstellen (optional)

## 🎯 Vorteile des Monorepos

### ✅ Code-Wiederverwendung
- Supabase-Client in mehreren Projekten nutzen
- Unipile-Client in mehreren Projekten nutzen
- Keine Code-Duplikation

### ✅ Zentrale Wartung
- Bug-Fixes an einer Stelle
- Updates propagieren zu allen Projekten

### ✅ Einfaches Testing
- Packages lokal testen
- Changes sofort sichtbar

### ✅ Versionierung
- Jedes Package hat eigene Version
- Semantic Versioning

## 📖 Dokumentation

- **Monorepo Overview:** [dev_packages/README.md](dev_packages/README.md)
- **Supabase Client:** [dev_packages/supabase-client/supabase_client/README.md](dev_packages/supabase-client/supabase_client/README.md)
- **Unipile Client:** [dev_packages/unipile-client/unipile_client/README.md](dev_packages/unipile-client/unipile_client/README.md)

## 🐛 Troubleshooting

### "Module not found"

```bash
# Packages neu installieren
pip install -e dev_packages/supabase-client
pip install -e dev_packages/unipile-client
```

### "Import error"

```python
# Richtige Imports verwenden
from supabase_api import SupabaseAPI  # ✅ Richtig
from supabase_client import SupabaseClient  # ❌ Falsch (low-level)
```

### Changes werden nicht übernommen

```bash
# Im editable mode sollten Changes sofort verfügbar sein
# Falls nicht:
pip uninstall supabase-client unipile-client
pip install -e dev_packages/supabase-client
pip install -e dev_packages/unipile-client
```

## 💡 Best Practices

1. **Editable Mode für Development:** `pip install -e .`
2. **Requirements aktuell halten:** Sync zwischen packages
3. **Versions-Tags nutzen:** Git Tags für Releases
4. **Dokumentation pflegen:** README.md aktualisieren
5. **Tests schreiben:** Vor größeren Änderungen

## 🚀 Quick Commands

```bash
# Setup (einmalig)
cd backend && ./install_packages.sh

# Update nach Änderungen (normalerweise nicht nötig)
pip install --upgrade -e dev_packages/supabase-client
pip install --upgrade -e dev_packages/unipile-client

# Package builden
cd dev_packages/supabase-client && python -m build

# Tests ausführen (wenn vorhanden)
cd dev_packages/supabase-client && pytest
```

---

Weitere Details: [dev_packages/README.md](dev_packages/README.md)
