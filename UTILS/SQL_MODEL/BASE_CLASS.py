from contextlib import contextmanager
from sqlmodel import SQLModel, create_engine, Session


class RootBase:
    def __init__(self, base_path: str, echo=False):
        self._engine = create_engine(f"sqlite:///{base_path}", echo=echo)
        SQLModel.metadata.create_all(bind=self._engine)

    @contextmanager
    def get_session(self):
        with Session(self._engine) as session:
            yield session
