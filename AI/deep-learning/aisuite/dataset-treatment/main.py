import os
import time
import pandas as pd
import unicodedata
import re
from sklearn.metrics import precision_score, recall_score, f1_score
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_community.llms import Ollama

df = pd.read_excel("processed_data.xlsx").head(10)

llm = Ollama(model="deepseek-r1:8b", temperature=0)

example_prompt = PromptTemplate.from_template(
    "Based on the text below, identify the corresponding medical specialty and respond only with its name in Portuguese. Do not include explanations, additional words, or special characters.\n\n"
    "{text}\n\n"
    "Resposta:"
)

examples = [
    {"text": "paciente em pós-operatório de endarterectomia de carótida com história prévia de AVC, solicito avaliação e acompanhamento", "label": "Fisioterapia"},
    {"text": "paciente com provável CEC de 8cm em região prétibial direita, autorizado encaixe no ambulatório da Dra. Madalena", "label": "Cirurgia Plástica"},
    {"text": "paciente em acompanhamento com cirurgia plástica por múltiplas lesões de câncer de pele, histórico de tarsal strip + retalho pediculado, suspeita de malignidade na pálpebra", "label": "Oftalmologia"},
    {"text": "paciente com síndrome demencial com necessidade de avaliação pela especialidade", "label": "Terapia Ocupacional"},
]

prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="{input}\n\nResposta:",
    input_variables=["input"],
)

def normalize_text(text):
    text = text.lower().strip()
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))

predicted_labels = []

print("\U0001F50D Classificando os textos...\n")

for index, row in df.iterrows():
    text = row['TEXTO_DO_SOLICITANTE']
    label = row['REQUISITADO']

    print(f"\U0001F4C4 Texto {index + 1}/{len(df)}:")
    print(f"\U0001F4DD {text}")
    print(f"\U0001F4CB Rótulo: {label}")
    print("⏳ Classificando...")

    try:
        prompt = prompt_template.invoke({"input": text}).to_string()
        prediction = llm.invoke(prompt).strip()
        prediction = normalize_text(prediction)

        if prediction == "fisiatria":
            prediction = "fisioterapia"
        elif " e " in prediction:
            prediction = "cirurgia geral"
        elif prediction == "nutricao":
            prediction = "nutricionista"
        elif "/" in prediction:
            prediction = prediction.split("/")[0]

    except Exception as e:
        prediction = "erro"
        print(f"⚠️ Erro ao classificar: {e}")

    print(f"✅ Especialidade Médica Prevista: {prediction}\n")

    predicted_labels.append(prediction)
    time.sleep(0.5)

df['Predicted_Label'] = predicted_labels
df['Label_First'] = df['REQUISITADO'].apply(lambda x: normalize_text(x.split('/')[0]))
df['Match'] = df.apply(lambda row: row['Predicted_Label'] in row['Label_First'], axis=1)

accuracy = df['Match'].mean()
precision = precision_score(df['Match'], [True] * len(df), average='binary', zero_division=0)
recall = recall_score(df['Match'], [True] * len(df), average='binary', zero_division=0)
f1 = f1_score(df['Match'], [True] * len(df), average='binary', zero_division=0)

print("\n\U0001F4CA Métricas de Desempenho:")
print(f"✅ Acurácia: {accuracy:.2f}")
print(f"✅ Precisão: {precision:.2f}")
print(f"✅ Revocação: {recall:.2f}")
print(f"✅ F1-Score: {f1:.2f}")

df.to_excel("classified_texts.xlsx", index=False)
print("\n✅ Arquivo classificado salvo como classified_texts.xlsx")