from sqlalchemy import create_engine, Column, Integer, String


engine = create_engine(
    url ="sqlite:///./sqlite.db", 
    echo=True,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables():
    """Create the database and tables."""
    from models import Shipment
    SQLModel.metadata.create_all(bind=engine)   



