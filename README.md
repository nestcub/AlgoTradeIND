# **AlgoTradeIND**  

AlgoTradeIND is a stock trading web application that provides **real-time price updates** using WebSockets and **technical indicator-based trading signals**. The app supports trading on **both the NASDAQ (US) and Nifty Fifty (India) markets**, ensuring that signals are generated according to their respective market timings.  

## **Features**  

- **Live Stock Price Updates:** Utilizes `yliveticker` WebSocket connections for real-time data.  
- **Signal Generation:** Uses `yfinance` to analyze 60 days of historical data and generate buy/sell signals.  
- **Responsive UI:** Built with **TailwindCSS** (installed locally) for a modern and clean interface.  
- **Paper Trading:** Practice buying and selling stocks based on dynamically generated trading signals.  

---

## **Usage**  

- **Live price updates** and **signal generation** are available even **without** the database setup.  
- If you only need real-time stock prices and trading signals, **you can skip the database setup**.  
- For full paper trading functionality, complete the **admin panel setup and user account creation**.  

---

## **Getting Started**  

### **1. Clone the Repository**  
```bash
git clone [project_url]
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

### **3. Set Up SQLite Database [ Skip to step 4 to avoid current database setup]**

Run the following commands to set up the database:  
```bash
python manage.py makemigrations
python manage.py migrate
```

Create a superuser for accessing the Django admin panel:  
```bash
python manage.py createsuperuser
```
Follow the prompts to set up a **username, email, and password**.

---

### **4. Set Up TailwindCSS**  

Open a **new terminal** in the project directory and run:  
```bash
npm install
```
This will install necessary TailwindCSS dependencies and create a `node_modules` folder.  

Start the TailwindCSS build process:  
```bash
npm run dev
```

---

### **5. Start the Django Server**  

Go back to the terminal where the Python virtual environment is activated and run:  
```bash
python manage.py runserver
```

---

### **6. Configure the Admin Panel**  

1. Open your browser and go to:  
   ```
   http://127.0.0.1:8000/admin/
   ```
2. Log in with the **superuser credentials** you created.  
3. Create a **user, add it to accounts** in the admin panel.  

---

### **7. Update `views.py`**  

Modify the following line in `views.py` to match the **username** you created in the admin panel.  
This line appears **twice** in different functions:  

```python
dummy_user = User.objects.get(username='test1')  # Change 'test1' to your created username
```

Once updated, you can now run the **paper trading model**.

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
