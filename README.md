# Dev Packages - Monorepo

Wiederverwendbare Python-Packages für mehrere Projekte.

## 📦 Verfügbare Packages

### 1. **supabase-client**
Modularer Supabase-Client mit vollständigen CRUD-Operationen.

**Features:**
- ✅ Vollständige CRUD-Operationen
- ✅ Modulare Architektur
- ✅ Tabellen-spezifische Services
- ✅ Such- und Filterfunktionen
- ✅ Wiederverwendbar über Projekte hinweg

**Dokumentation:** [supabase-client/README.md](supabase-client/supabase_client/README.md)

### 2. **unipile-client**
Unipile API-Client für LinkedIn-Profile.

**Features:**
- ✅ Eigenes LinkedIn-Profil abrufen
- ✅ Fremde LinkedIn-Profile abrufen
- ✅ Modulare Architektur
- ✅ Wiederverwendbar über Projekte hinweg

**Dokumentation:** [unipile-client/README.md](unipile-client/unipile_client/README.md)

---

## 🚀 Installation

### Option 1: Lokale Installation (Development)

Jedes Package kann lokal im "editable mode" installiert werden:

```bash
# Supabase Client
cd dev_packages/supabase-client
pip install -e .

# Unipile Client
cd dev_packages/unipile-client
pip install -e .
```

**Vorteil:** Änderungen am Code sind sofort verfügbar, ohne Neuinstallation.

### Option 2: Installation aus dev_packages

```bash
# Supabase Client
pip install -e dev_packages/supabase-client

# Unipile Client
pip install -e dev_packages/unipile-client
```

### Option 3: Installation aus Git (für andere Projekte)

```bash
# Via pip direkt aus diesem Repo
pip install git+https://github.com/yourusername/yourrepo.git#subdirectory=dev_packages/supabase-client
pip install git+https://github.com/yourusername/yourrepo.git#subdirectory=dev_packages/unipile-client
```

### Option 4: Build und Installation (Production)

```bash
# Supabase Client builden
cd dev_packages/supabase-client
python -m build
pip install dist/supabase_client-1.0.0-py3-none-any.whl

# Unipile Client builden
cd dev_packages/unipile-client
python -m build
pip install dist/unipile_client-1.0.0-py3-none-any.whl
```

---

## 📁 Projektstruktur

```
dev_packages/
│
├── README.md                      # Diese Datei
│
├── supabase-client/               # Supabase Package
│   ├── supabase_client/           # Python Package
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── config.py
│   │   ├── services/
│   │   ├── models/
│   │   └── utils/
│   ├── supabase_api.py            # Haupt-API
│   ├── examples/                  # Beispiele
│   ├── setup.py                   # Setup-Konfiguration
│   ├── pyproject.toml             # Moderne Setup-Konfiguration
│   ├── MANIFEST.in                # Distribution-Dateien
│   ├── LICENSE                    # MIT License
│   ├── README.md                  # Package-Dokumentation
│   └── requirements_supabase.txt  # Dependencies
│
└── unipile-client/                # Unipile Package
    ├── unipile_client/            # Python Package
    │   ├── __init__.py
    │   ├── client.py
    │   ├── config.py
    │   └── profiles.py
    ├── unipile_api.py             # Haupt-API
    ├── examples/                  # Beispiele
    ├── setup.py                   # Setup-Konfiguration
    ├── pyproject.toml             # Moderne Setup-Konfiguration
    ├── MANIFEST.in                # Distribution-Dateien
    ├── LICENSE                    # MIT License
    └── README.md                  # Package-Dokumentation
```

---

## 🎯 Verwendung in Projekten

### In diesem Projekt (linkedin_social_selling)

```python
# Im Backend
from supabase_api import SupabaseAPI
from unipile_api import UnipileAPI

# Initialisieren
supabase = SupabaseAPI.from_env()
unipile = UnipileAPI.from_env()

# Verwenden
result = supabase.table('users').get_all()
result = unipile.profiles.get_own_profile(account_id="...")
```

### In anderen Projekten

Nach Installation der Packages:

```python
# Projekt A
from supabase_api import SupabaseAPI
api = SupabaseAPI.from_env()

# Projekt B
from unipile_api import UnipileAPI
api = UnipileAPI.from_env()

# Projekt C - beide verwenden
from supabase_api import SupabaseAPI
from unipile_api import UnipileAPI

supabase = SupabaseAPI.from_env()
unipile = UnipileAPI.from_env()
```

---

## 🔧 Development Workflow

### 1. Neues Package hinzufügen

```bash
# Neue Package-Struktur erstellen
mkdir -p dev_packages/new-package/new_package
cd dev_packages/new-package

# Setup-Dateien erstellen
touch setup.py pyproject.toml MANIFEST.in LICENSE README.md
touch new_package/__init__.py
```

### 2. Package entwickeln

```bash
# Im editable mode installieren
pip install -e dev_packages/new-package

# Änderungen sind sofort verfügbar
# Kein Re-Install nötig
```

### 3. Package testen

```bash
# Tests für Supabase
cd dev_packages/supabase-client
python -m pytest tests/

# Tests für Unipile
cd dev_packages/unipile-client
python -m pytest tests/
```

### 4. Package builden

```bash
# Build tools installieren
pip install build twine

# Package builden
cd dev_packages/supabase-client
python -m build

# Erstellt:
# - dist/supabase_client-1.0.0-py3-none-any.whl
# - dist/supabase-client-1.0.0.tar.gz
```

### 5. Package veröffentlichen (optional)

```bash
# Auf PyPI veröffentlichen
python -m twine upload dist/*

# Auf privatem PyPI-Server
python -m twine upload --repository-url https://your-pypi-server.com dist/*
```

---

## 📋 Requirements Management

### Development Dependencies

```bash
# Für Package-Entwicklung
pip install -e "dev_packages/supabase-client[dev]"
pip install -e "dev_packages/unipile-client[dev]"

# Beinhaltet:
# - pytest
# - black (Code-Formatting)
# - flake8 (Linting)
```

### Production Dependencies

Werden automatisch mit dem Package installiert.

**Supabase Client:**
- supabase>=2.3.4
- python-dotenv>=1.0.0

**Unipile Client:**
- requests>=2.31.0
- python-dotenv>=1.0.0

---

## 🎓 Best Practices

### 1. **Versions-Management**

```python
# In __init__.py
__version__ = "1.0.0"

# In setup.py und pyproject.toml synchron halten
version = "1.0.0"
```

### 2. **Dependencies sparsam halten**

Nur wirklich benötigte Dependencies hinzufügen.

### 3. **Tests schreiben**

```bash
dev_packages/supabase-client/
├── tests/
│   ├── test_client.py
│   ├── test_services.py
│   └── test_models.py
```

### 4. **Dokumentation aktuell halten**

Bei Änderungen:
- README.md updaten
- Docstrings aktualisieren
- Beispiele anpassen

### 5. **Semantic Versioning**

- **1.0.0** → **1.0.1**: Bug-Fixes
- **1.0.0** → **1.1.0**: Neue Features (abwärtskompatibel)
- **1.0.0** → **2.0.0**: Breaking Changes

---

## 🔄 Updates zwischen Projekten

### Package in diesem Projekt aktualisieren

```bash
# Im Hauptprojekt
cd linkedin_social_selling
pip install --upgrade -e dev_packages/supabase-client
```

### Package in anderem Projekt aktualisieren

```bash
# Via Git
pip install --upgrade git+https://github.com/yourusername/yourrepo.git#subdirectory=dev_packages/supabase-client

# Via lokalen Pfad (wenn gecloned)
pip install --upgrade -e /path/to/linkedin_social_selling/dev_packages/supabase-client
```

---

## 🚀 CI/CD Integration

### GitHub Actions Beispiel

```yaml
# .github/workflows/test-packages.yml
name: Test Packages

on: [push, pull_request]

jobs:
  test-supabase:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install package
        run: |
          pip install -e "dev_packages/supabase-client[dev]"
      - name: Run tests
        run: |
          cd dev_packages/supabase-client
          pytest tests/

  test-unipile:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install package
        run: |
          pip install -e "dev_packages/unipile-client[dev]"
      - name: Run tests
        run: |
          cd dev_packages/unipile-client
          pytest tests/
```

---

## 📖 Weitere Ressourcen

- **Python Packaging Guide:** https://packaging.python.org/
- **Semantic Versioning:** https://semver.org/
- **Monorepo Best Practices:** https://monorepo.tools/

---

## 🎯 Quick Commands

```bash
# Alle Packages im Development-Mode installieren
pip install -e dev_packages/supabase-client
pip install -e dev_packages/unipile-client

# Alle Packages mit Dev-Dependencies installieren
pip install -e "dev_packages/supabase-client[dev]"
pip install -e "dev_packages/unipile-client[dev]"

# Alle Packages builden
cd dev_packages/supabase-client && python -m build && cd ../..
cd dev_packages/unipile-client && python -m build && cd ../..

# Tests für alle Packages ausführen
cd dev_packages/supabase-client && pytest && cd ../..
cd dev_packages/unipile-client && pytest && cd ../..
```

---

## 💡 Tipps

1. **Editable Mode verwenden:** `pip install -e .` für Development
2. **Requirements trennen:** Production vs. Development Dependencies
3. **Versions-Tags nutzen:** Git Tags für Package-Versionen
4. **CHANGELOG führen:** Änderungen dokumentieren
5. **Tests schreiben:** Vor jedem Release

---

Viel Erfolg mit Ihrem Monorepo! 🎉
