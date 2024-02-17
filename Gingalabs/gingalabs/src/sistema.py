import json
import openai
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()
client = openai.OpenAI(
    api_key=os.environ['OPENAI'],
)

class Sistema:
    def __init__(self):
        self.supabase_url = os.environ["SUPABASE_PROJECT"]
        self.supabase_key = os.environ["SUPABASE_API_KEY"]
        self.supabase = create_client(self.supabase_url, self.supabase_key)
        self.vendedor_logado = None

    #check
    def fazer_login(self, username, email):
        response = self.supabase.from_('users').select('*').eq('username', username).eq('email', email).execute()
        try:
            if response:
                user_data = response.dict()
                self.vendedor_logado = {
                        "UserID": user_data['data'][0]['userid'],
                        "Username": user_data['data'][0]['username']
                    }
                return True
            else:
                return False
        except IndexError:
            print("Erro ao realizar a verficação do usuário. Credenciais inválidas!")

    def _verificar_login(self):
        if not self.vendedor_logado:
            raise Exception("Você precisa fazer login para executar esta operação.")

    #check
    def consultar_informacoes(self):
        self._verificar_login()
        response = self.supabase.table('products').select('*').eq('owneruserid', self.vendedor_logado["UserID"]).execute()
        
        if response:
            print("Informações dos seus produtos:")
            response = dict(response)

            user_json_path = f'{os.path.abspath(os.getcwd()).replace("\\", "/")}/Gingalabs/gingalabs/Logs/json/{self.vendedor_logado["Username"]}.json'

            user_data = {"produtos": response['data']}

            with open(user_json_path, 'w') as json_file:
                json.dump(user_data, json_file, indent=2)

            print(f'Dados salvos em: {user_json_path}')
            
            for produto in response['data']:
                for coluna, valor in produto.items():
                    print(f'"{coluna}": "{valor}"')
            print()
        else:
            print("Nenhum produto encontrado para este vendedor.")
        
        return response
    
    #check
    def ranking_produtos_mais_vendidos(self):
        response = self.supabase.table('products').select('productname', 'sales').order('sales', desc=True).execute()
        response = dict(response)
        if response:
            print("Ranking de produtos mais vendidos:")
            
            for produto in response['data']:
                print(f'Nome do produto: {produto['productname']} -> Total de vendas:{produto['sales']}')
            print()
        else:
            print("Nenhum produto encontrado.")
        
        return response
    
    def cadastrar_novo_produto(self, nome, categoria):
        self._verificar_login()
        novo_produto = {
            "ProductName": nome,
            "Category": categoria,
            "OwnerUserID": self.vendedor_logado["UserID"]
        }

        response = self.supabase.from_('produtos').upsert([novo_produto]).execute()

        if response.status_code == 201:
            return response.json()
        return None
    
    def obter_sugestao_reposicao_estoque(self):
        self._verificar_login()

        # Consultar produtos com estoque baixo considerando <= 10
        response = self.supabase.table('products').select('productname', 'sales').eq('owneruserid', self.vendedor_logado["UserID"]).lte('stockquantity', 10).execute()

        products = dict(response)

        for produto in products['data']:
            if products:
                prompt = f"Os seguintes produtos estão com estoque baixo e precisam ser repostos: {', '.join(produto['productname'])}."
            else:
                prompt = "Todos os seus produtos têm estoque suficiente. Não é necessário repor no momento."
        print()

        # Obter sugestão da OpenAI
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50
        )

        return response.choices[0].text.strip()


    def obter_sugestao_novos_produtos(self):
        self._verificar_login()
        prompt = "Quais novos produtos você poderia considerar vender?"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50
        )
        return response.choices[0].text.strip()
