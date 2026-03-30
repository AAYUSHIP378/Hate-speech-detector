from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# ---------------- DATABASE URL ----------------
DATABASE_URL = "sqlite:///./predictions.db"

# ---------------- ENGINE ----------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

# ---------------- SESSION ----------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ---------------- BASE ----------------
Base = declarative_base()

# ---------------- MODEL ----------------
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    text = Column(String, nullable=False)

    prediction = Column(String, index=True)
    hate_type = Column(String, index=True)

    confidence = Column(Float)

    language = Column(String, index=True)

    model = Column(String)

    action = Column(String, index=True)   # ✅ FIXED (यहीं होना चाहिए)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

    def __repr__(self):
        return f"<Prediction(id={self.id}, prediction={self.prediction}, confidence={self.confidence})>"

# ---------------- CREATE TABLE ----------------
def init_db():
    Base.metadata.create_all(bind=engine)