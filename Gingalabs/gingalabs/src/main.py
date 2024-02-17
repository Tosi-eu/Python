from sistema import Sistema
     
def menu():
    print("\nSelecione uma opção:")
    print("1. Fazer login")
    print("2. Consultar informações de produtos")
    print("3. Ver ranking de produtos mais vendidos")
    print("4. Cadastrar novo produto")
    print("5. Obter sugestão de reposição de estoque")
    print("6. Obter sugestão de novos produtos")
    print("7. Sair")

if __name__ == "__main__":
    marketplace_system = Sistema()

    while True:

        menu()
        escolha = input("Opção: ")
        match escolha:
            case "1":
                # Fazer login
                username = input("Digite seu username: ")
                password = input("Digite sua senha: ")
                if marketplace_system.fazer_login(username, password):
                    print(f"Bem-vindo, {username}!")
            
            case "2":
                # Consultar informações de produtos
                marketplace_system.consultar_informacoes()

            case "3":
                # Ver ranking de produtos mais vendidos
                ranking = marketplace_system.ranking_produtos_mais_vendidos()
                print("Ranking de produtos mais vendidos:")
                for produto in ranking:
                    print(produto)

            case "4":
                # Cadastrar novo produto
                nome_produto = input("Digite o nome do novo produto: ")
                categoria_produto = input("Digite a categoria do novo produto: ")
                novo_produto = marketplace_system.cadastrar_novo_produto(nome_produto, categoria_produto)
                if novo_produto:
                    print(f"Novo produto cadastrado com sucesso: {novo_produto}")
                else:
                    print("Falha ao cadastrar o novo produto. Verifique os dados.")

            case "5":
                # Obter sugestão de reposição de estoque
                sugestao_reposicao = marketplace_system.obter_sugestao_reposicao_estoque()
                print(f"Sugestão de reposição de estoque: {sugestao_reposicao}")

            case "6":
                # Obter sugestão de novos produtos
                sugestao_novos_produtos = marketplace_system.obter_sugestao_novos_produtos()
                print(f"Sugestão de novos produtos: {sugestao_novos_produtos}")

            case "7":
                # Sair do loop
                print("Saindo do sistema. Até logo!")
                break

            case _:
                print("Opção inválida. Tente novamente.")
