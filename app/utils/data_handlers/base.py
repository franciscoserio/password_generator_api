from sqlalchemy.orm import Session


class BaseDataHandler:
    def __init__(self, db: Session) -> None:
        self.db: Session = db
