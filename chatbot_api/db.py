from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:qwe123@localhost/chatbot"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@contextmanager
def my_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from sqlalchemy import Column, Integer, String, Text
import os
import json
import sys


class QAPair(Base):
    __tablename__ = "qa_pairs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    type = Column(String, nullable=True)


def create_qa_pairs_table():
    Base.metadata.create_all(bind=engine)


def add_data_from_json_to_db(db, json_folder_path: str):
    for filename in os.listdir(json_folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(json_folder_path, filename)
            with open(file_path, "r") as file:
                qa_pairs = json.load(file)
                for pair in qa_pairs:
                    db_pair = QAPair(
                        question=pair["question"],
                        answer=pair["answer"],
                        type=pair.get("type", None),
                    )
                    db.add(db_pair)
            db.commit()


def main(json_folder_path: str):
    # Create the table if it does not exist
    create_qa_pairs_table()

    # Add data from JSON files to the table
    with SessionLocal() as db:
        add_data_from_json_to_db(db, json_folder_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python db.py <path_to_json_folder>")
    else:
        json_folder_path = sys.argv[1]
        main(json_folder_path)
