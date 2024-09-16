import pandas as pd
from sqlalchemy import func
from sqlalchemy.orm import Session
from db import QAPair
from utils import convert_numpy_int64


def count_questions_by_type(db: Session) -> pd.DataFrame:
    """
    Return the number of questions for each type.

    :param db: Database session
    :return: DataFrame with question types and their counts
    """
    results = db.query(QAPair.type, func.count(QAPair.id)).group_by(QAPair.type).all()
    df = pd.DataFrame(results, columns=["type", "count"])
    data = df.to_dict(orient="records")
    return convert_numpy_int64(data)


def get_qa_pairs_sample(db: Session) -> pd.DataFrame:
    """
    Return a sample of 5 rows from the qa_pairs table.

    :param db: Database session
    :return: DataFrame with 5 rows from the qa_pairs table
    """
    results = db.query(QAPair).limit(5).all()
    df = pd.DataFrame(
        [
            {
                "id": pair.id,
                "question": pair.question,
                "answer": pair.answer,
                "type": pair.type,
            }
            for pair in results
        ]
    )
    data = df.to_dict(orient="records")
    return convert_numpy_int64(data)


FUNC_MAP = {
    "count_questions_by_type": {"method": count_questions_by_type, "type": "chart"},
    "get_qa_pairs_sample": {"method": get_qa_pairs_sample, "type": "table"},
}
