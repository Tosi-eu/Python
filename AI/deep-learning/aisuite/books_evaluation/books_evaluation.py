from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from datasets import load_dataset
import json
from os import makedirs, getenv

api_key = getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

dataset = load_dataset("BrightData/Goodreads-Books", split="train")
dataset = dataset.train_test_split(test_size=0.5)
test_data = dataset["test"].shuffle(seed=42).select(range(100))

# Define the evaluation prompt
evaluation_prompt = PromptTemplate(
    input_variables=["genres", "author", "summary", "star_rating"],
    template=(
        "You are a book evaluation expert. Based on the provided genre, author, summary, and star rating, "
        "evaluate whether the book is a good purchase or not. Consider that star_rating bigger or equal than 3.5 are good purchases. "
        "Create a review that includes a brief evaluation of the book's main points and your reasoning for the decision.\n\n"
        "Provided Criteria:\n"
        "Genre: {genres}\n"
        "Author: {author}\n"
        "Summary: {summary}\n"
        "Star Rating: {star_rating}\n\n"
        "Decision: (Answer if the book is good to buy or not and explain the reason.)\n"
    ),
)

# Create individual chains
evaluation_chain = evaluation_prompt | llm 

# Function to evaluate books
def evaluate_books(data, evaluation_chain):
    results = []
    titles = []
    for entry in data:
        title = entry.get("name", "Unknown")
        genres = entry.get("genres", [])
        author = entry.get("author", [])
        summary = entry.get("summary", "No summary available.")
        star_rating = entry.get("star_rating", 0)
        
        if genres:
            evaluation = evaluation_chain.invoke({
                "genres": genres,
                "author": author,
                "summary": summary,
                "star_rating": star_rating,
                "book_titles": title,
            })

            print(evaluation.content)
            exit(1)
            
            results.append({
                "title": title,
                "genres": genres,
                "author": author,
                "summary": summary,
                "star_rating": star_rating,
                "decision": evaluation.content,
            })

            titles.append(title)

    return results, titles

evaluated_books, book_titles = evaluate_books(test_data, evaluation_chain)

output_folder = "books_evaluation/results"
makedirs(output_folder, exist_ok=True)

output_path = f"{output_folder}/evaluated_books.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(evaluated_books, f, indent=4, ensure_ascii=False)

print(f"Resultados salvos em {output_path}")
