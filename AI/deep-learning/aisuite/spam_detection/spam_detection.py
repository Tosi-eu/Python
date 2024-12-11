import json
import random
from datasets import load_dataset
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from pandas import DataFrame
from os import makedirs 

api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.9, api_key=api_key)
spam_sms = []
non_spam_sms = []

dataset = load_dataset("sms_spam")

dataset = dataset["train"].train_test_split(test_size=0.5)
test_data = dataset["test"].shuffle(42).select(range(150))

prompt = PromptTemplate(
    input_variables=["sms"],
    template=(
        "You are an expert in spam detection. Classify the following SMS "
        "strictly as 'Spam' or 'Not Spam'. Avoid providing any additional text "
        "in the classification. Additionally, identify the key words or phrases "
        "that justify the classification.\n\n"
        "SMS: {sms}\n\n"
        "Classification: (strictly 'Spam' or 'Not Spam')\n\n"
        "Key words/phrases: (provide a comma-separated list)"
    ),
)
chain = prompt | llm
keywords = []  

correct_predictions = 0  
for i, sample in enumerate(test_data):
    sms = sample["sms"]
    true_label = "Spam" if sample["label"] == 1 else "Not Spam"
    
    input_variables = {
        "sms": sms,
    }

    response_text = chain.invoke(input_variables).content.strip()

    predicted_label = response_text.split("Classification:")[-1].split("\n")[0].strip()

    keywords_raw = response_text.split("Key words/phrases:")[-1].strip()
    extracted_keywords = [word.strip() for word in keywords_raw.split(",") if word.strip()]

    for keyword in extracted_keywords:
        keywords.append({"word": keyword, "label": predicted_label})

    if true_label.lower() == predicted_label.lower():
        correct_predictions += 1

    print(f"\nSMS {i+1}:\nSMS: {sms}\n"
          f"True Classification: {true_label}\n"
          f"Predicted Classification: {predicted_label}\n"
          f"Extracted Keywords: {extracted_keywords}\n")
    
        # Store SMS in respective category list
    if predicted_label == "Spam":
        spam_sms.append({"sms": sms, "true_label": true_label, "predicted_label": predicted_label, "keywords": extracted_keywords})
    else:
        non_spam_sms.append({"sms": sms, "true_label": true_label, "predicted_label": predicted_label, "keywords": extracted_keywords})


accuracy = correct_predictions / len(test_data)
print(f"\nAccuracy on test set: {accuracy:.2%}")

keywords_df = DataFrame(keywords)

word_counts = keywords_df['word'].value_counts()
keywords_df['count'] = keywords_df['word'].map(word_counts)

keywords_df['color'] = keywords_df['label'].apply(lambda x: 'red' if x == 'Spam' else 'green')

keywords_df['x'] = keywords_df['label'].apply(lambda x: random.uniform(0, 5) if x == 'Spam' else random.uniform(5, 10))
keywords_df['y'] = [random.uniform(0, 10) for _ in range(len(keywords_df))]

output_dir = "output"
makedirs(output_dir, exist_ok=True)

spam_file = os.path.join(output_dir, "spam_sms.json")
non_spam_file = os.path.join(output_dir, "non_spam_sms.json")

with open(spam_file, 'w', encoding='utf-8') as f:
    json.dump(spam_sms, f, ensure_ascii=False, indent=4)

with open(non_spam_file, 'w', encoding='utf-8') as f:
    json.dump(non_spam_sms, f, ensure_ascii=False, indent=4)