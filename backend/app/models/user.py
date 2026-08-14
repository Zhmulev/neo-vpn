from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timedelta
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Триал
    trial_start = Column(DateTime, default=datetime.utcnow)
    trial_end = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=3))
    is_trial_used = Column(Boolean, default=False)

    # Прокси
    proxy_enabled = Column(Boolean, default=False)
    proxy_limit = Column(Integer, default=1)

    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email}>"