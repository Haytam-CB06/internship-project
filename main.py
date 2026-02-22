from fastapi import FastAPI,Request,UploadFile, File
from fastapi.responses import HTMLResponse,JSONResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json,bcrypt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import pandas as pd
import io
ADMIN_SECRET_CODE = "SECRET123" 
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
app = FastAPI()

origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
 
class graphdata(BaseModel):
   Xaxis : str
   Yaxis: str



class UserSignUp(BaseModel):
    username: str
    password: str
    role: str
    admin_code: str = ""  # optional
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()

def transform_passwords(input_file="users.json", output_file="users.json"):
    with open(input_file, "r") as f:
        users = json.load(f)

    for user in users:
        # Only hash if the password is not already hashed
        if not user["password"].startswith("$2b$"):
            user["password"] = hash_password(user["password"])

    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)
transform_passwords() 



def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)


def load_users(file_path="users.json"):
    with open(file_path, "r") as f:
        return json.load(f)

global uploaded_data 
uploaded_data = None
@app.get("/get_graph_data")
async def get_graph_data():
    if not uploaded_data:
        return JSONResponse(status_code=404, content={"error": "No data uploaded yet"})
    return uploaded_data


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    global uploaded_data
    try:
        contents = await file.read()
        filename = file.filename.lower()
        
        if filename.endswith(".json"):
            uploaded_data = json.loads(contents.decode())
            
        elif filename.endswith(".csv"):
    # Convert CSV to JSON using pandas with proper configuration
            try:
                    df = pd.read_csv(
                    io.StringIO(contents.decode('utf-8')),
                    quotechar='"',
                    escapechar='\\',
                    dtype=str,  # Read all as strings initially
                    keep_default_na=False,  # Don't convert empty strings to NaN
                    na_values=[''],  # Explicitly handle empty strings
                    parse_dates=False  # Don't try to parse dates automatically
                )
                # Convert all columns to strings to prevent type issues
                    df = df.astype(str)
                    uploaded_data = df.replace('nan', '').to_dict(orient="records")
            except Exception as e:
                    return JSONResponse(
                    status_code=400,
                    content={"error": f"Failed to parse CSV: {str(e)}"}
                )
            
        elif filename.endswith(".xlsx"):
            # Ensure you have openpyxl installed: pip install openpyxl
            df = pd.read_excel(io.BytesIO(contents))
            uploaded_data = df.to_dict(orient="records")
            
        else:
            return JSONResponse(
                status_code=400,
                content={"error": "Unsupported file format"}
            )
            
        return {"message": "File converted to JSON", "data": uploaded_data}
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to process file: {str(e)}"}
        )





@app.get("/test", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})



@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})



@app.get("/admin_dashboard",response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})




@app.get("/user_dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse("user_dashboard.html", {"request": request})



@app.get("/about", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})




@app.get("/services", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("services.html", {"request": request})




@app.get("/contact", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})



@app.get("/signup", response_class=HTMLResponse)
def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})



@app.get("/login",response_class=HTMLResponse)
def home(req:Request):
    return templates.TemplateResponse("login.html", {"request": req})


@app.post("/login")
async def login(request: Request):
    body = await request.json()
    username = body["username"]
    password = body["password"]
    print("User submitted:", username, password)
    print("Looking for username in users.json...")

    users=load_users()
    
    print("Loaded users:", users)
    
    if not all([username, password]):
        return JSONResponse({"message": "Missing required fields"}, status_code=400)

    # Check if username exists
    user = next((user_ for user_ in users if user_["username"] == username), None)
    print("Matched user:", user)
    if not user:
        return JSONResponse(content={ "message": "username not found"}, status_code=401)

    # Check password
    if not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return JSONResponse(content={ "message": "Incorrect password"}, status_code=401)
    # Check if user or admin
    
    #check admin
    return JSONResponse({"message": "Login successful","role": user["role"]}, status_code=200)



@app.post("/signup")
async def signup(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"detail": "Invalid JSON format"}, status_code=400)

    username = data.get("username")
    password = data.get("password")
    confirm = data.get("cpassword")
    role = data.get("role")
    admin_code = data.get("admin_code")
    
    # Basic validation
    if not all([username, password, confirm, role]):
        return JSONResponse({"detail": "Missing required fields"}, status_code=400)

    if role=="admin" and admin_code!=ADMIN_SECRET_CODE:
        return JSONResponse({"detail": "ADMIN SECRET CODE IS INCORRECT"}, status_code=400)

    # Load users
    try:
        users = load_users()
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    # Check duplicate
    if any(u["username"] == username for u in users):
        return JSONResponse({"detail": "Username already exists"}, status_code=400)

    # Admin code validation
    if role == "admin" and admin_code != ADMIN_SECRET_CODE:
        return JSONResponse({"detail": "Invalid admin code"}, status_code=403)

    # Hash password
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    users.append({
        "username": username,
        "password": hashed_pw,
        "role": role
    })

    save_users(users)

    return JSONResponse({"message": "Signup successful"}, status_code=200)
