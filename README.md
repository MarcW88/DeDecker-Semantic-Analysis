# SEO Intelligence Dashboard

Dashboard SEO custom basé sur Streamlit, connecté à Google Search Console et DataForSEO.

## 🏗️ Architecture

```
dashboard_seo/
│
├── app.py                    # Application Streamlit principale
├── config.py                 # Configuration
├── requirements.txt          # Dépendances Python
│
├── connectors/               # Connecteurs API
│   ├── gsc.py               # Google Search Console
│   └── dataforseo.py        # DataForSEO
│
├── pipelines/                # Pipelines de traitement
│   ├── opportunity_finder.py # Détection d'opportunités
│   ├── semantic_clusters.py  # Analyse de clusters
│   └── serp_monitor.py       # Monitoring SERP
│
├── database/                 # Base de données
│   └── models.py            # Modèles SQLAlchemy
│
└── data/                     # Données locales
```

## 🚀 Installation

```bash
# Cloner le projet
cd dashboard_seo

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos credentials
```

## ⚙️ Configuration

### Google Search Console

1. Créer un projet Google Cloud
2. Activer l'API Search Console
3. Créer un compte de service
4. Télécharger le fichier JSON des credentials
5. Ajouter le compte de service comme utilisateur dans GSC

### DataForSEO

1. Créer un compte sur [DataForSEO](https://dataforseo.com)
2. Récupérer vos credentials API
3. Ajouter dans `.env`

### Base de données (optionnel)

```bash
# Créer une base PostgreSQL
createdb seo_dashboard

# Configurer DATABASE_URL dans .env
```

## 🎯 Lancement

```bash
streamlit run app.py
```

Le dashboard sera accessible sur `http://localhost:8501`

## 📊 Modules

### 1. Overview
- KPIs principaux (clicks, impressions, position, CTR)
- Tendances de trafic
- Top opportunités

### 2. Opportunity Finder
- Quick wins (position 6-20, high impressions)
- CTR opportunities
- Striking distance keywords
- Cannibalization detection

### 3. Semantic Clusters
- Clustering automatique par n-grams
- Analyse de couverture
- Identification des gaps

### 4. SERP Monitoring
- Volatilité SERP
- Part de voix concurrents
- SERP features tracking

### 5. AI Visibility
- Présence dans AI Overviews
- Citations de marque
- Tracking GEO

## 🔧 Personnalisation par client

1. Ajouter le client via l'interface
2. Connecter la propriété GSC
3. Configurer les keywords à monitorer
4. Les données sont stockées par client

## 📈 Roadmap

- [ ] Embeddings pour clustering avancé
- [ ] Alertes automatiques
- [ ] Export PDF/Excel
- [ ] API REST pour intégrations
- [ ] Multi-utilisateurs

## 📝 License

MIT
