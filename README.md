# cynaris-internship-data-analytics.

Data analytics internship project .

## Week 3 Day 4 — Looker Studio

- **Dashboard:** [Cynaris Sales Dashboard](https://datastudio.google.com/reporting/43475023-9491-44ba-a826-d7d3245607bc)
- **Screenshot:** `python-pandas/screenshots/looker_studio_dashboard.png`
- **Data source:** Google Sheets
- **Charts:** Scorecard, bar chart, line chart, pie chart, and table
- **Interactive filters:** Region and Category

---

## Production Deployment

FastAPI-based CIA data analyst with CSV upload, PandasAI/Groq analysis, interactive charts, executive summaries, and PowerPoint export.

### Deployment

Render configuration: `render.yaml`. Install dependencies using `pip install -r requirements.txt`. Set `GROQ_API_KEY` in Render environment settings; never commit the key.

Deployment URL: Pending deployment.

### API documentation

FastAPI interactive documentation: `/docs`. Alternative documentation: `/redoc`.

### Known limitations

- CSV upload limit: 10 MB.
- Sessions are held in memory and are lost when the application restarts.
- Use one application instance; sessions are not shared between instances.
- AI features require a valid Groq API key.
- Chart.js is loaded from a CDN.
