# 🏛️ CivicPulse: Local Body Grievance & Monitoring Portal

CivicPulse is a lightweight, full-stack web application designed to streamline grassroots infrastructure reporting and resolution for local administrative bodies (such as town panchayats and municipal wards). 

It bridges the gap between everyday citizens and municipal authorities by replacing manual paper registers or scattered messaging apps with transparent, real-time ticket tracking and data-driven administrative analytics.

---

## ✨ Key Features

* **📝 Citizen Complaint Lodging:** Citizens can easily report localized infrastructure bottlenecks (Streetlights, Water Supply, Sanitation, Roads, Drainage) with location landmarks and contact details.
* **🔍 Real-Time Ticket Tracking:** Generates a unique Tracking ID (`TKT-YYYYMMDDHHMMSS`) allowing citizens to inspect live progress, resolution status, and officer remarks anytime.
* **📊 Municipal Admin Dashboard:** Secured dashboard for officers to view incoming complaint queues, update statuses (*Pending* ➔ *In Progress* ➔ *Resolved*), log action notes, and analyze ward-wise performance metrics.
* **📈 Operational Analytics:** Built-in charts and metrics highlighting high-priority zones and issue categories using Pandas and Streamlit.

---

## 🛠️ Tech Stack

* **Frontend & UI:** Python, Streamlit
* **Database & Backend:** SQLite (`sqlite3`), Pandas
* **Deployment:** Streamlit Community Cloud & GitHub

---

## 🚀 Local Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/sujithraghav28-web/YOUR_REPOSITORY_NAME.git](https://github.com/sujithraghav28-web/YOUR_REPOSITORY_NAME.git)
   cd YOUR_REPOSITORY_NAME
