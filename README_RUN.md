# How to Run NyayLens

## Quick Start (Easiest Method)

### Windows Users
Simply double-click one of these files:
- **`start.bat`** - Opens servers in separate command windows
- **`start.ps1`** - PowerShell version (right-click → Run with PowerShell)

Both scripts will:
1. Start the backend server on http://localhost:8001
2. Start the frontend server on http://localhost:5500
3. Automatically open the application in your browser

---

## Manual Start

### Option 1: Using VS Code Terminal

1. **Start Backend:**
   ```powershell
   cd D:\pil26
   D:/pil26/.venv/Scripts/python.exe -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001
   ```

2. **Start Frontend (in a new terminal):**
   ```powershell
   cd D:\pil26\frontend
   D:/pil26/.venv/Scripts/python.exe -m http.server 5500 --bind 127.0.0.1
   ```

3. **Open Browser:**
   - Navigate to http://localhost:5500

### Option 2: Using Command Prompt

1. Open Command Prompt and run:
   ```batch
   cd D:\pil26
   .venv\Scripts\python.exe -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001
   ```

2. Open another Command Prompt and run:
   ```batch
   cd D:\pil26\frontend
   .venv\Scripts\python.exe -m http.server 5500 --bind 127.0.0.1
   ```

---

## Access Points

Once running, you can access:

- **Frontend Application:** http://localhost:5500
- **Backend API:** http://localhost:8001
- **API Documentation (Swagger):** http://localhost:8001/docs
- **API Documentation (ReDoc):** http://localhost:8001/redoc

---

## Troubleshooting

### "Failed to fetch" Error
- Make sure BOTH servers are running
- Check that you're accessing http://localhost:5500 (not file://)
- Verify backend is on http://localhost:8001

### Port Already in Use
- **Port 8001:** Another backend instance is running
- **Port 5500:** Another frontend instance is running
- Solution: Close existing instances or change ports in the startup scripts

### Virtual Environment Not Found
- Ensure you've installed dependencies:
  ```powershell
  python -m venv .venv
  .venv\Scripts\activate
  pip install -r requirements.txt
  ```

---

## Stopping the Servers

- **If using start.bat/start.ps1:** Close the terminal windows
- **If using VS Code terminal:** Press `Ctrl+C` in each terminal
- **If using Command Prompt:** Press `Ctrl+C` in each window

---

## First Time Setup

If you haven't set up the project yet:

1. **Clone/Download the repository**
2. **Create virtual environment:**
   ```powershell
   python -m venv .venv
   ```
3. **Activate it:**
   ```powershell
   .venv\Scripts\activate
   ```
4. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```
5. **Run the project:**
   - Double-click `start.bat`
