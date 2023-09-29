from sqlmodel import Session, create_engine


from backend.app import settings


db_connection_str = settings.db_connection_str

engine = create_engine(
    db_connection_str,
    echo=True
)


def get_session():
    with Session(engine) as session:
        yield session

