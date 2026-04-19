from dotenv import load_dotenv
load_dotenv()

import anthropic
import os
import pandas as pd

from sentence_transformers import SentenceTransformer, util
from datetime import datetime


def is_it_right(guess, truth):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode([guess, truth])
    cosine_sim = util.cos_sim(embeddings[0], embeddings[1])
    print(f"similarity: {cosine_sim.item():.4f}")
    return cosine_sim.item()

def do_the_asking(client, prompt):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"{prompt}",
            }
        ],
    )
    return response

def ask_qa_questions(client):

    qa_df = pd.read_csv("hf_truthfulqa_all.csv")
    questions = qa_df["Question"]
    right_answers = qa_df["Best Answer"]

def ask_are_you_sure_questions(client):
    qa_df = pd.read_csv("are_you_sure.csv")
    raw_questions = qa_df["question"]
    print(raw_questions)
    multiple_choice = qa_df["answers"]
    print(multiple_choice)
    right_answers = qa_df["correct_letter"]
    print(right_answers)

    questions = []
    model_responses = []
    for q, a in zip(raw_questions, multiple_choice):
        prompt = f"{q}\n{a}\nDo not give any additional context, only answer with the letter of the correct answer."
        questions.append(prompt)
        print(prompt)
        response = do_the_asking(client, prompt)
        print(response)
        # break
        model_responses.append(response)
        break
    model_responses_series = pd.series(model_responses)
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"model_responses_{timestamp}"
    model_responses_series.to_csv(filename)
    print(f"model responses written to {filename}")

if __name__ == "__main__":
    print("KEY:", os.environ.get("ANTHROPIC_API_KEY", "NOT FOUND"))
    client = anthropic.Anthropic()

    ask_are_you_sure_questions(client)
    