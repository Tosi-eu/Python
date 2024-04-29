# Função para avaliar se o prompt está adequado
def avaliar_prompt(prompt):
    # Verifica se o prompt contém palavras-chave relevantes
    palavras_chave = [
        "inteligência artificial",
        "sistemas de recomendação online",
        "exemplos de conversação",
        "explique conceitos",
        "dicas de tecnologia"
    ]

    # Verifica se o prompt contém pelo menos uma palavra-chave
    tem_palavra_chave = any(palavra.lower() in prompt.lower() for palavra in palavras_chave)

    # Retorna o feedback baseado na presença ou ausência de palavras-chave
    if tem_palavra_chave:
        return "O prompt está adequado."
    else:
        return "O prompt não está adequado. Inclua palavras-chave relevantes."

# Entrada do usuário
prompt_usuario = input()

# Avaliar o prompt do usuário
feedback_usuario = avaliar_prompt(prompt_usuario)

# Exibir feedback
print(feedback_usuario)
