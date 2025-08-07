# 🏐 Volleyball NYC Events Scraper & Web App

This project scrapes event data from [volleyball-nyc.com](https://www.volleyball-nyc.com/events) and displays upcoming volleyball events in a clean, friendly interface. You can run this app locally to stay up to date with NYC volleyball events, including location, time, level, and direct registration links.

---

## 🧠 Features

- Scrapes latest volleyball events from Volleyball NYC
- Parses event title, time, level, cost, availability, and address
- Saves event data to a local SQLite database
- Provides an API and a React-based web frontend to view events
- Refreshes data with a single button click

---

## 🛠 Tech Stack

- **Backend**: FastAPI, Selenium, BeautifulSoup, SQLite (via SQLAlchemy)
- **Frontend**: React + Vite
- **Database**: SQLite

---

## 🚀 Getting Started Locally

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/volleyball-nyc-scraper.git
cd volleyball-nyc-scraper
```

### 🐍 Backend Setup (FastAPI + Selenium)
### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
Make sure Chrome and ChromeDriver are installed and match in version.

### 4. Start the Backend Server

```bash
uvicorn main:app --reload
```
This runs the backend server at:

📍 http://localhost:8000
📮 http://localhost:8000/docs — FastAPI interactive API docs

To trigger a fresh scrape:
```bash
curl -X POST http://localhost:8000/refresh
```

### 🌐 Frontend Setup (React + Vite)
### 5. Go to the frontend folder

```bash
cd frontend
```

### 6. Install Node Dependencies

```bash
npm install
```

### 7. Run the Development Server
```bash
npm run dev
```
Visit the frontend in your browser:
📺 http://localhost:5173

Make sure your backend is running on port 8000.

---

## 🗃️ Database Info
- Data is stored in events.db (SQLite)
- You don’t need to create the database manually — it will be created on first run
- Events are inserted using SQLAlchemy models

---

## 📁 Folder Structure
volleyball-nyc-scraper/
├── main.py                  # FastAPI app
├── requirements.txt         # Python backend deps
├── events.db                # SQLite database (auto-generated)
├── scraper/
│   └── volleyball_nyc.py    # Selenium scraping logic
├── database/
│   ├── models.py
│   ├── insert_event.py
│   └── db.py
├── frontend/
│   ├── index.html
│   └── src/                 # React code
└── README.md                # You are here!

---

## 💡 Development Notes
	•	If you get a stale element error in Selenium, it often helps to re-locate elements inside the loop, or wait longer using time.sleep()
	•	You can edit the scraping logic in scraper/volleyball_nyc.py
	•	Inserting into the DB is handled in database/insert_event.py

---

## ❤️ Credits
Built with care by volleyball lover Azalea Sun who lived in the in NYC area for 3 years and played volleyball in all 5 boros 😁
Special thanks to ChatGPT for assiting me with debugging and brainstorming 💗
Feel free to fork, contribute, or reach out!

---

## 🧪 Future Improvements
	•	Add better duplicate filtering
	•	Add new organization scraping
	•	Improve health checks and debugging mechanisms