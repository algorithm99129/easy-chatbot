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


FUNC_MAP = {
    "count_questions_by_type": {"method": count_questions_by_type, "type": "table"}
}
