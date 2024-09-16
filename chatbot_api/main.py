from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
from fastapi.middleware.cors import CORSMiddleware
import json
import uvicorn
from db import get_db, QAPair, my_db
from sqlalchemy.orm import Session

from db_analysis_functions import FUNC_MAP
from utils import convert_numpy_int64

FUNC_KEY = "[method]:"

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model once at startup
model = SentenceTransformer("./model")


class ChatRequest(BaseModel):
    message: str
    type: str


def load_qa_pairs(filename: str):
    """Load QA pairs from a JSON file."""
    try:
        with open(filename, "r") as file:
            qa_pairs = json.load(file)
        return qa_pairs
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"File {filename} not found.")
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail=f"Error decoding JSON from file {filename}."
        )


def prepare_embeddings(qa_pairs: List[QAPair]):
    """Prepare embeddings for the questions in the QA pairs."""
    questions = [pair.question for pair in qa_pairs]
    question_embeddings = model.encode(questions, convert_to_tensor=True)
    return questions, question_embeddings


def get_most_similar_answer(user_question: str, question_embeddings, qa_pairs: list):
    """Find the most similar answer to the user's question."""
    user_question_embedding = model.encode(user_question, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(user_question_embedding, question_embeddings)
    best_match_idx = similarities.argmax().item()
    return qa_pairs[best_match_idx].answer


def load_qa_pairs_from_db(db: Session, type: str = None):
    """Load QA pairs from the database."""
    query = db.query(QAPair)
    if type:
        query = query.filter(QAPair.type == type)
    return query.all()


@app.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Chat endpoint to get the most similar answer based on user role and question.
    """
    user_role = request.type.lower()
    if user_role not in ["customer", "seller"]:
        raise HTTPException(
            status_code=400, detail="Invalid type. Must be 'customer' or 'seller'."
        )

    if user_role == "customer":
        answer = get_most_similar_answer(
            request.message, question_embeddings_customer, qa_pairs_customer
        )
    else:
        answer = get_most_similar_answer(
            request.message, question_embeddings_seller, qa_pairs_seller
        )

    answer = str(answer)
    type = "text"
    if answer.startswith(FUNC_KEY):
        func_name = answer[len(FUNC_KEY) :]
        data = FUNC_MAP[func_name]["method"](db=db)
        type = FUNC_MAP[func_name]["type"]
        return JSONResponse(content={"data": data, "type": type})

    return {"answer": answer, "type": type}


if __name__ == "__main__":
    global qa_pairs_customer, question_embeddings_customer
    global qa_pairs_seller, question_embeddings_seller

    with my_db() as db:
        greetings = load_qa_pairs_from_db(db, type=None)

        qa_pairs_customer = load_qa_pairs_from_db(db, type="customer") + greetings
        questions_customer, question_embeddings_customer = prepare_embeddings(
            qa_pairs_customer
        )

        qa_pairs_seller = load_qa_pairs_from_db(db, type="seller") + greetings
        questions_seller, question_embeddings_seller = prepare_embeddings(
            qa_pairs_seller
        )

    uvicorn.run(app, host="0.0.0.0", port=8000)
