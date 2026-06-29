# 🏙️ Urban Data Explorer

## 📖 Description

Urban Data Explorer est une plateforme décisionnelle permettant d'analyser le marché immobilier parisien à partir de plusieurs sources Open Data.

L'application aide différents profils d'utilisateurs à :

- 🏠 Acheter
- 📈 Investir
- ❤️ Habiter
- 👴 Préparer sa retraite

grâce à des indicateurs métiers calculés automatiquement.

---

## 🚀 Fonctionnalités

- Carte interactive de Paris
- Comparaison de deux arrondissements
- Timeline des prix immobiliers
- Analyse automatique
- KPI dynamiques
- Plusieurs indicateurs métiers

---

## 🏗️ Architecture

Open Data
      │
      ▼
Python + Pandas
      │
      ▼
SQLite (Silver)
      │
      ▼
Calcul des indicateurs
      │
      ▼
MongoDB (Gold)
      │
      ▼
FastAPI
      │
      ▼
React + Leaflet

---

## 🛠️ Technologies

- Python
- Pandas
- SQLite
- MongoDB
- FastAPI
- React
- Leaflet

---

## 📂 Structure du projet

backend/

frontend/

scripts/

data/

docs/

---

## ⚙️ Installation

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
## Frontend
cd frontend
npm install
npm run dev

## Lancer le pipeline
python run_pipeline.py

## Auteur
Projet réalisé dans le cadre du Master Data Engineering.
