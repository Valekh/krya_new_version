from sqlalchemy import INT, Column, String, create_engine, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/krya")
Session = sessionmaker(autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class BotSpeech(Base):
    __tablename__= "bot_speech"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text = Column(String)
    keyword = Column(String, nullable=True)
    image = Column(String, nullable=True)

class Chat(Base):
    __tablename__= "chat"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger)
    status = Column(String)


Base.metadata.create_all(bind=engine)

