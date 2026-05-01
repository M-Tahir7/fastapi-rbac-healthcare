from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm,HTTPAuthorizationCredentials,HTTPBearer
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import bcrypt
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()
Database_url = os.getenv("DATABASE_URL")
engine = create_engine(Database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Role(BaseModel):
    admin: str = "admin"
    doctor: str = "doctor"
    patient: str = "patient"

roles = Role()


class RegisterUser(BaseModel):
    username: str
    password: str
    role: str

# ===========================
# Database Models
# ===========================
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)  # store role as string: admin/doctor/patient

class DoctorDetail(Base):
    __tablename__ = "doctor_details"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    speciality = Column(String)
    user = relationship("User")

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("users.id"))
    patient_id = Column(Integer, ForeignKey("users.id"))
    date = Column(String)  # For simplicity; in production use DateTime
    doctor = relationship("User", foreign_keys=[doctor_id])
    patient = relationship("User", foreign_keys=[patient_id])

Base.metadata.create_all(bind=engine)


app = FastAPI()
secret_key = os.getenv("SECRET_KEY")
Algorithm = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = HTTPBearer()
# ===========================
# Helper Functions
# ===========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, Algorithm)

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def get_password_hash(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

def get_current_user(credential: HTTPAuthorizationCredentials = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        token = credential.credentials
        payload = jwt.decode(token, secret_key, algorithms=[Algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def role_required(required_roles: list[str]):
    def wrapper(user: User = Depends(get_current_user)):
        if user.role not in required_roles:
            raise HTTPException(status_code=403, detail="Access forbidden for your role")
        return user
    return wrapper

# ===========================
# Registration & Login
# ===========================

@app.post("/register")
def register(user: RegisterUser, db: Session = Depends(get_db)):
    if user.role not in [roles.admin, roles.doctor, roles.patient]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User created successfully", "user_id": new_user.id}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer","Message":"Login Successful"}

# ===========================
# Role-Based Endpoints
# ===========================

# Doctor: See upcoming appointments & patient details
@app.get("/doctor/appointments")
def doctor_appointments(user: User = Depends(role_required([roles.doctor, roles.admin])), db: Session = Depends(get_db)):
    appointments = db.query(Appointment).filter(Appointment.doctor_id == user.id).all()
    result = []
    for a in appointments:
        patient = db.query(User).filter(User.id == a.patient_id).first()
        result.append({"appointment_id": a.id, "date": a.date, "patient_name": patient.username})
    return result

# Patient: See list of doctors with speciality
@app.get("/patient/doctors")
def patient_doctors(user: User = Depends(role_required([roles.patient, roles.admin])), db: Session = Depends(get_db)):
    doctors = db.query(User).filter(User.role == roles.doctor).all()
    result = []
    for d in doctors:
        doc_detail = db.query(DoctorDetail).filter(DoctorDetail.user_id == d.id).first()
        result.append({"doctor_name": d.username, "speciality": doc_detail.speciality if doc_detail else "N/A"})
    return result

# Admin: Access all users
@app.get("/admin/all-users")
def all_users(user: User = Depends(role_required([roles.admin])), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "username": u.username, "role": u.role} for u in users]
