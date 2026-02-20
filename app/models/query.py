from sqlalchemy import column, Integer, String, Date, Boolean
from app.core.database import Base

class query(Base):
    __tablename__ = "queries"

    id = column(Integer, primary_key=True, index=True)
    query_text = column(String, index=True)
    reponse =   column(String)
    created_at = column(Date)
