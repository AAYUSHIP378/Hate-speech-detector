from fastapi import FastAPI, Form, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.model import predict
from app.database import SessionLocal, Prediction, init_db

# ---------------- APP ----------------
app = FastAPI()

# ---------------- MIDDLEWARE ----------------
app.add_middleware(SessionMiddleware, secret_key="secret")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- TEMPLATES ----------------
templates = Jinja2Templates(directory="app/templates")

# ---------------- STARTUP ----------------
@app.on_event("startup")
def startup():
    init_db()

# ---------------- DB ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- HOME ----------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ---------------- ANALYZE ----------------
@app.post("/analyze", response_class=HTMLResponse)
def analyze(request: Request, text: str = Form(...), db: Session = Depends(get_db)):

    result = predict(text)

    # ✅ Save to DB
    record = Prediction(**result)
    db.add(record)
    db.commit()

    return templates.TemplateResponse("result.html", {
        "request": request,
        "result": result
    })

# ---------------- LOGIN ----------------
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):

    if username == "admin" and password == "admin123":
        request.session["admin"] = True
        return RedirectResponse("/dashboard", status_code=303)

    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": "Invalid Credentials"
    })

# ---------------- LOGOUT ----------------
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)

# ---------------- DASHBOARD ----------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):

    if not request.session.get("admin"):
        return RedirectResponse("/login", status_code=303)

    rows = db.query(Prediction).all()

    total = len(rows)
    hate = len([r for r in rows if r.prediction == "Hate Speech"])
    non_hate = total - hate

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "rows": rows,
        "total": total,
        "hate": hate,
        "non_hate": non_hate
    })

# ---------------- DELETE ----------------
@app.get("/delete/{id}")
def delete(id: int, request: Request, db: Session = Depends(get_db)):

    if not request.session.get("admin"):
        return RedirectResponse("/login", status_code=303)

    row = db.query(Prediction).filter(Prediction.id == id).first()

    if row:
        db.delete(row)
        db.commit()

    return RedirectResponse("/dashboard", status_code=303)

# ---------------- STATS ----------------
@app.get("/stats")
def stats(db: Session = Depends(get_db)):

    total = db.query(Prediction).count()
    hate = db.query(Prediction).filter(Prediction.prediction == "Hate Speech").count()

    return {
        "total": total,
        "hate": hate,
        "non_hate": total - hate
    }