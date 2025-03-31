# **AlgoTradeIND**  

AlgoTradeIND is a stock trading web application that provides **real-time price updates** using WebSockets and **technical indicator-based trading signals**. The app supports trading on **both the NASDAQ (US) and Nifty Fifty (India) markets**, ensuring that signals are generated according to their respective market timings.  

## **Features**  

- **Live Stock Price Updates:** Utilizes `yliveticker` WebSocket connections for real-time data.  
- **Signal Generation:** Uses `yfinance` to analyze 60 days of historical data and generate buy/sell signals.  
- **Responsive UI:** Built with **TailwindCSS** (installed locally) for a modern and clean interface.  
- **Paper Trading:** Practice buying and selling stocks based on dynamically generated trading signals.  

---

## **Getting Started**  

### **1. Clone the Repository**  
```bash
git clone [this project_url]
cd AlgoTradeIND
```

### **2. Set Up Python Virtual Environment**  

Create and activate a virtual environment:  
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

Install dependencies:  
```bash
pip install -r requirements.txt
```

### **3. Set Up TailwindCSS**  

Open a **new terminal** in the project directory and run:  
```bash
npm install
```
This will install necessary TailwindCSS dependencies and create a `node_modules` folder.  

Start the TailwindCSS build process:  
```bash
npm run dev
```

### **4. Start the Django Server**  

Go back to the terminal where the Python virtual environment is activated and run:  
```bash
python manage.py runserver
```

Your application should now be running! 🎉  

---

## **Usage**  

- The app provides real-time stock price updates and **buy/sell signals** based on technical indicators in `utils.py`.  
- Supports **NASDAQ (US)** and **Nifty Fifty (India)** markets.  
- Ensure that you run the application **during the respective market hours** for accurate price data and signals.  

---

## **Tech Stack**  

- **Backend:** Django, WebSockets (`yliveticker`), `yfinance`  
- **Frontend:** Django Templates, TailwindCSS  
- **Database:** SQLite (default) or PostgreSQL (optional)  

---

## **Contributing**  

Contributions are welcome! Please follow these steps:  
1. Fork the repository  
2. Create a new branch (`feature-branch`)  
3. Commit your changes  
4. Open a pull request  

---
