from vendedor import Vendedor

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
    vendedor = Vendedor()

    while True:
        menu()
        try:
            escolha = input("Opção: ")
            match escolha:
                case "1":
                    # Fazer login
                    vendedor.fazer_login()
                case "2":
                    # Consultar informações de produtos
                    vendedor.consultar_informacoes()
                case "3":
                    # Ver ranking de produtos mais vendidos
                    vendedor.ranking_produtos_mais_vendidos()
                case "4":
                    # Cadastrar novo produto
                    vendedor.cadastrar_novo_produto()
                case "5":
                    # Obter sugestão de reposição de estoque
                    sugestao_reposicao = vendedor.obter_sugestao_reposicao_estoque()
                    print(f"Sugestão de reposição de produtos: {sugestao_reposicao}")
                case "6":
                    # Obter sugestão de novos produtos
                    sugestao_novos_produtos = vendedor.obter_sugestao_novos_produtos()
                    print(f"Sugestão de novos produtos: {sugestao_novos_produtos}")
                case "7":
                    # Sair do loop
                    print("Saindo do sistema. Até logo!")
                    break
                case _:
                    print("Opção inválida. Tente novamente.")
                    
        except IOError as io:
            print("Probelma com entrada ou saída: !", io)
        except ValueError as ve:
            print("Entrada inválida!")
        except Exception as e:
            print("Erro desconhecido: ", e)
