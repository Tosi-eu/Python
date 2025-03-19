import re
import pandas as pd

df = pd.read_excel('HCFMB-REL-2022-00048.xls')

df = df.fillna('')

regex = re.compile(r"[^\w\s/+]", re.UNICODE)

remove_words_regex = re.compile(r"\b(atenciosamente|att|grato|grata|obrigado|obrigada|obg|bom dia|por gentileza)\b", re.IGNORECASE)

phone_regex = re.compile(r"\(?\d{2}\)?\s?9\d{3}-?\d{4}")

df_merged = df.groupby(['RG', 'CD_ATENDIMENTO', 'DATA_SOLICITACAO'], as_index=False).agg({
    'REQUISITADO': lambda x: '/'.join(sorted(set(x))),
    'TEXTO_DO_SOLICITANTE': 'first'  
})

def remove_special_chars_from_text(text):
    if isinstance(text, str):
        text = text.replace("\n", " ").replace("\r", " ")
        return regex.sub("", text)
    return text

def transform_text_to_lower(text):
    if isinstance(text, str):
        return text.lower()
    return text

def clean_text(text):
    if isinstance(text, str):
        text = remove_words_regex.sub("", text)
        text = phone_regex.sub("", text) 
        text = re.sub(r"\bpcte\b", "paciente", text)  
        text = re.sub(r"\s+", " ", text).strip() 
        return text
    return text

def clean_label(label):
    label = re.sub(r"\b(\w+)\s+clinica\b", r"\1", label)  
    label = label.replace(" e ", "/")
    return label

df_merged['REQUISITADO'] = df_merged['REQUISITADO'].apply(remove_special_chars_from_text).apply(transform_text_to_lower)
df_merged['TEXTO_DO_SOLICITANTE'] = df_merged['TEXTO_DO_SOLICITANTE'].apply(remove_special_chars_from_text).apply(transform_text_to_lower)

df_merged['TEXTO_DO_SOLICITANTE'] = df_merged['TEXTO_DO_SOLICITANTE'].apply(clean_text)

df_merged['REQUISITADO'] = df_merged['REQUISITADO'].apply(clean_label)
df_merged['REQUISITADO'] = df_merged['REQUISITADO'].replace('cirurgia vascular', 'reumatologia')
df_merged['REQUISITADO'] = df_merged['REQUISITADO'].replace('cirurgia pediatrica', 'pediatria')

df_merged.to_excel('processed_data.xlsx', index=False)