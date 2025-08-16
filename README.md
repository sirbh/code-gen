# 🚀 Setup Guide

## Prerequisites
- **Python 3.11+**
- **Docker & Docker Compose**
- **Node.js 18+**

---

## 1. Check Python Version
Make sure you’re using **Python 3.11 or later** (required for LangGraph compatibility).  
Run:
```bash
python3 --version
```

---



### Create an environment and install dependencies
#### Mac/Linux/WSL
```
$ python3 -m venv code-gen-env
$ source code-gen-env/bin/activate
$ pip install -r requirements.txt
```
#### Windows Powershell
```
PS> python3 -m venv code-gen-env
PS> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
PS> code-gen-env\scripts\activate
PS> pip install -r requirements.txt
```

### Configure environment variables
Create a `.env` file in the backend root and add:
```env
OPENAI_API_KEY="your_api_key_here"
```

---

### Run the backend
```bash
python run.py
```

---

## 3. Frontend Setup
From the project root:
```bash
cd frontend
npm install
npm run dev
```

---

## 4. Access the App
The app will now be live at:  
👉 [http://localhost:3000](http://localhost:3000)

---

# 🛠 Usage Guide

Once the app is running:

1. **Generate OpenAPI Spec**  
   - The app will first ask you to generate an OpenAPI specification.

2. **Validate the Spec (optional)**  
   - You may be prompted to validate the generated spec.

3. **Save the Spec**  
   - Save the file and confirm it exists in the root directory with the name:  
     ```
     openapi.json
     ```

4. **Generate Server Code**  
   - Click **Generate Server Code**.  
   - Confirm that a new directory called:
     ```
     server_code
     ```
     has been created.

5. **Test the Generated Server**  
   - You can now test the generated server with actions like:
     - Running Docker Compose  
     - Viewing logs  
     - Making API requests  
     - Updating code

---


## ✅ Notes
- Ensure you have **Node.js 18+** installed for the frontend.  
- If you face issues activating the Python environment on Windows, try:
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  ```
- If `npm install` fails due to permissions, run:
  ```bash
  npm install --legacy-peer-deps
  ```


