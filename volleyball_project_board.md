
# NYC Volleyball Aggregator – Project Board

## ✅ Phase 1: Web Scrapers
- [x] Big City Volleyball scraper
- [x] Volleyball NYC scraper
- [ ] Volo Sports scraper
  - [ ] Test if direct URL access is possible
  - [ ] If not, simulate search interaction with Selenium
- [ ] (Optional) Add more data sources

## 🗄️ Phase 2: Data Storage
- [ ] Choose database (SQLite for local / PostgreSQL for production)
- [ ] Design table schema
- [ ] Save scraper data to DB
- [ ] Handle duplicates (upsert or dedup)

## 🚪 Phase 3: Backend API
- [ ] Choose framework (e.g. FastAPI)
- [ ] Build endpoints:
  - [ ] `GET /events`
  - [ ] `GET /events?date=&location=`
  - [ ] `POST /refresh`
- [ ] Connect API to frontend

## ⏰ Phase 4: Scheduling
- [ ] Local auto-updates with `schedule` or `APScheduler`
- [ ] Define update frequency
- [ ] Deploy background jobs or cron

## 🌈 Phase 5: Frontend UI
- [ ] Use Next.js + Tailwind
- [ ] Design layout (list / filters / details)
- [ ] Highlight Full vs Open events
- [ ] Link to registration page

## ☁️ Phase 6: Deployment
- [ ] Deploy backend (Render / Railway)
- [ ] Deploy frontend (Vercel)
- [ ] Connect to database
- [ ] Test everything end-to-end

## 🧋 Phase 7: Optional Features
- [ ] Admin dashboard
- [ ] Favoriting / Tagging
- [ ] Export to calendar

## 💼 Bonus: Portfolio Polish
- [ ] Write README
- [ ] Add to GitHub & resume
