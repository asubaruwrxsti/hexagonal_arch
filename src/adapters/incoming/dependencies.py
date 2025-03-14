from adapters.outgoing.database import Database

def get_db():
    db = Database()
    db_session = next(db.get_session())
    try:
        yield db_session
    finally:
        db_session.close()