# Flickr.io

A monorepo content intelligence dashboard for exploring movie and streaming data — ratings,
genres, release trends, and audience preferences across Netflix, Prime Video, and Disney+.

**No AI/ML. No external API dependency. Powered entirely by Kaggle CSV datasets.**

---

## Project Structure

```
flickr.io/
├── backend/          # Python FastAPI + SQLite
│   ├── app/          # FastAPI application
│   ├── scripts/      # Data ingestion script
│   └── data/         # Kaggle CSVs (git-ignored)
└── frontend/         # Vue 3 + Vuetify + Chart.js
    └── src/
        ├── views/    # 6 page views
        ├── components/  # Reusable chart + UI components
        └── api/      # Axios client
```

---

## Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| Data Source  | Kaggle CSV (Netflix / Prime / Disney+) |
| Ingestion    | Python + pandas                     |
| Database     | SQLite                              |
| Backend      | Python FastAPI + SQLAlchemy Core    |
| Frontend     | Vue 3 + Vuetify 3 + Chart.js        |
| Deployment   | Railway / Render (backend) + Vercel (frontend) |

---

## Prerequisites

- Python 3.10+
- Node.js 18+

---

## 1 — Download Kaggle Datasets

Download the following CSV files and place them in `backend/data/`:

| Platform  | Kaggle Dataset                                  | Expected filename           |
|-----------|-------------------------------------------------|-----------------------------|
| Netflix   | [Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows) | `netflix_titles.csv`        |
| Prime     | [Amazon Prime Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/amazon-prime-movies-and-tv-shows) | `amazon_prime_titles.csv`   |
| Disney+   | [Disney+ Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/disney-movies-and-tv-shows) | `disney_plus_titles.csv`    |

> A sample `netflix_titles.csv` with 12 rows is included for local testing.

---

## 2 — Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# Install dependencies
pip install -r requirements.txt
```

---

## 3 — Ingest Data

Run the ingestion script once per platform. It creates `backend/app/flickrio.db` automatically.

```bash
# From the backend/ directory (with venv active)
python scripts/ingest.py --platform netflix
python scripts/ingest.py --platform prime
python scripts/ingest.py --platform disney
```

The script is idempotent — re-running it will not create duplicate rows.

> **Note:** The SQLite DB file lives inside the container when deployed to Railway/Render.
> Data resets on every redeploy unless a persistent volume is attached. For the MVP,
> commit a pre-seeded `flickrio.db` to the repo or re-run the ingest script after each deploy.

---

## 4 — Run the Backend (Development)

```bash
# From the backend/ directory (with venv active)
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API docs available at: **http://localhost:8000/docs**

---

## 5 — Frontend Setup & Dev Server

```bash
cd frontend

# Install dependencies (first time only)
npm install

# Copy the example env file
cp .env.example .env

# Start dev server
npm run dev
```

App available at: **http://localhost:5173**

---

## 6 — Environment Variables

### Frontend (`frontend/.env`)

| Variable       | Default                  | Description                                  |
|----------------|--------------------------|----------------------------------------------|
| `VITE_API_URL` | `http://localhost:8000`  | Base URL of the deployed or local backend    |

Set `VITE_API_URL` to your Railway/Render backend URL before building for production.

---

## 7 — Deployment

### Backend → Railway

1. Push the repo to GitHub.
2. Create a new Railway project → **Deploy from GitHub repo**.
3. Set the **Root Directory** to `backend/`.
4. Railway auto-detects `railway.json` — no further config needed.
5. After deploy, open a Railway shell and run the ingest script:
   ```bash
   python scripts/ingest.py --platform netflix
   ```

### Backend → Render

1. Create a new **Web Service** on Render.
2. Set **Root Directory** to `backend/`.
3. Render auto-detects `render.yaml`.
4. After deploy, use the Render Shell to run the ingest script.

### Frontend → Vercel

1. Import the repo on Vercel.
2. Set **Root Directory** to `frontend/`.
3. Vercel auto-detects `vercel.json` — build command `npm run build`, output `dist/`.
4. Add environment variable `VITE_API_URL` → your backend's public URL.
5. Deploy.

---

## API Reference

| Endpoint                  | Description                                         |
|---------------------------|-----------------------------------------------------|
| `GET /health`             | Health check                                        |
| `GET /api/ratings`        | Content rating distribution (`?platform=&type=`)    |
| `GET /api/genres`         | Genre counts (`?platform=&release_year=`)           |
| `GET /api/releases`       | Titles per year (`?platform=&type=`)                |
| `GET /api/trends`         | Most recent titles (`?platform=&genre=&limit=`)     |
| `GET /api/search`         | Title search (`?q=&platform=&limit=`)               |

Full interactive docs: `http://localhost:8000/docs`

---

## Out of Scope (MVP)

- No AI/ML (no recommendations, predictions, or NLP)
- No user accounts or authentication
- No real-time data ingestion
- No TMDb / OMDb live API integration
- No PostgreSQL migration
