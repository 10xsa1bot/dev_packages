# Google PageSpeed Insights Python Package

Ein Python-Package zum Abrufen von Daten aus der Google PageSpeed Insights API.

## Installation

```bash
pip install -e .
```

## Verwendung

```python
from google_pagespeed_insights import PageSpeedClient

# Client initialisieren
client = PageSpeedClient(api_key="YOUR_API_KEY")

# URL analysieren
result = client.analyze_url("https://example.com", strategy="mobile")

print(result)
# {
#     "success": True,
#     "url": "https://example.com",
#     "scores": {
#         "performance": 85.5,
#         "accessibility": 92.0,
#         "best_practices": 88.0,
#         "seo": 95.0
#     },
#     "metrics": {...}
# }
```

## API Key erhalten

1. Gehe zu [Google Cloud Console](https://console.cloud.google.com/)
2. Erstelle ein neues Projekt oder wähle ein existierendes
3. Aktiviere die PageSpeed Insights API
4. Erstelle API-Credentials (API Key)
5. Kopiere den API Key

## Features

- Performance Score
- Accessibility Score
- Best Practices Score
- SEO Score
- Core Web Vitals Metriken
