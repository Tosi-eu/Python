from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain.memory import SimpleMemory
from datetime import datetime
from os import getenv
from datasets import load_dataset
import json
from os import makedirs

# Load the StackOverflow dataset
dataset = load_dataset("mikex86/stackoverflow-posts", split="train")
dataset = dataset.shuffle(seed=42).select(range(100))  # Selecting a subset for the demo

# Define the LLM to be used
llm = OpenAI(model="gpt-3.5-turbo", api_key=getenv("OPENAI_API_KEY"))

# --------- First Prompt: Evaluate Posts ---------

# Evaluation template for StackOverflow posts
evaluation_template: str = """You are an expert in evaluating StackOverflow posts. Based on the provided title, body, tags, and score, 
evaluate whether the post is of high quality or not. Consider the score to be a significant factor—posts with scores greater than 10 
are considered high quality. Additionally, assess the clarity and completeness of the post content.

Please provide a brief evaluation of the post with your reasoning.

Post Details:
Title: {title}
Body: {body}
Tags: {tags}
Score: {score}

Evaluation: (Is the post high quality or not and explain why?)\
"""

evaluation_prompt_template = PromptTemplate(
    input_variables=["title", "body", "tags", "score"], template=evaluation_template)

# Creating the evaluation chain
evaluation_chain: LLMChain = LLMChain(
    llm=llm, output_key="evaluation", prompt=evaluation_prompt_template)


# --------- Second Prompt: Group Posts by Similarity ---------

# Grouping template based on similarity (e.g., grouping by tags or content similarity)
grouping_template: str = """You are a StackOverflow expert. Based on the provided tags, group the posts into categories based on shared topics or themes.
If posts share similar tags or content, group them together. List the groups with their respective titles.

Please provide the groups in the following format:
1. Group Name: Topic
   Titles: [Title 1, Title 2, ...]

Posts and Tags:
{posts_and_tags}

Group the posts accordingly.
"""

grouping_prompt_template = PromptTemplate(
    input_variables=["posts_and_tags"], template=grouping_template)

# Creating the grouping chain
grouping_chain: LLMChain = LLMChain(
    llm=llm, output_key="grouped_posts", prompt=grouping_prompt_template)


# --------- Final Output Chain ---------

# Final output template to format the evaluated and grouped posts
final_template: str = """You are responsible for providing the final quality-assured evaluation and grouping of StackOverflow posts.

Your final response should be in the following format:

Evaluation Result: {evaluation_result}
Groupings: {groupings}

Here are the details:
{grouped_posts}
"""

final_prompt_template = PromptTemplate(
    input_variables=["evaluation_result", "groupings", "grouped_posts"], template=final_template)

# Creating the final chain
final_chain: LLMChain = LLMChain(
    llm=llm, output_key="final_output", prompt=final_prompt_template)


# --------- Complete Chain ---------

# Creating a simple sequential chain to run the full process
ss_chain: SequentialChain = SequentialChain(
    memory=SimpleMemory(memories={"time_created_and_verified": str(datetime.utcnow())}),
    chains=[evaluation_chain, grouping_chain, final_chain],
    input_variables=["title", "body", "tags", "score"],
    output_variables=["final_output"],
    verbose=True)

# --------- Function to Process Posts ---------

def process_posts(data, chain):
    results = []
    for entry in data:
        title = entry.get("Title", "Unknown Title")
        body = entry.get("Body", "No body provided.")
        tags = entry.get("Tags", [])
        score = entry.get("Score", 0)

        # Run the full chain to evaluate and group posts
        final_output = chain.run(
            title=title, body=body, tags=tags, score=score)

        # Collect the final output for each post
        results.append(final_output)
    
    return results


# Run the process
processed_posts = process_posts(dataset, ss_chain)

# Output the results
output_folder = "stackoverflow_post_evaluations"
makedirs(output_folder, exist_ok=True)

output_path = f"{output_folder}/processed_posts.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(processed_posts, f, indent=4, ensure_ascii=False)

print(f"Processed results saved in {output_path}")
