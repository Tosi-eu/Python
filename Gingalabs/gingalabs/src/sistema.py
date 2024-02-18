import json
import random
import re
from openai import OpenAI
from dotenv import load_dotenv
import os
import postgrest
from supabase import create_client

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

class Sistema:
    def __init__(self):
        self.supabase_url = os.environ["SUPABASE_PROJECT"]
        self.supabase_key = os.environ["SUPABASE_API_KEY"]
        self.supabase = create_client(self.supabase_url, self.supabase_key)
        self.online= None

    #check
    def sign_in(self):
        # Fazer login
        username = input("Digite seu username: ")
        email = input("Digite seu email: ")
        response = self.supabase.from_('users').select('*').eq('username', username).eq('email', email).execute()

        try:
            if response:
                user_data = response.dict()
                self.online = {
                        "UserID": user_data['data'][0]['userid'],
                        "Username": user_data['data'][0]['username']
                    }
                return True
            else:
                return False
        except IndexError:
            print("Erro ao realizar a verficação do usuário. Credenciais inválidas!")

    #check
    def _verify_login(self):
        if not self.online:
            print("Usuário não está logado, preecha seus dados para prosseguir!")
            self.sign_in()

    #check
    def _validate_product_name(self, nome):
        pattern = re.compile(r'^[a-zA-Z0-9 _áéíóúâêîôûãõàèìòùäëïöüç]*$')

        if pattern.match(nome):
            return True
        else:
            return False
  
    #check
    def consult_informations(self):
        self._verify_login()
        response = self.supabase.table('products').select('*').eq('owneruserid', self.online["UserID"]).execute()
        
        if response:
            print("Informações dos seus products:")
            response = dict(response)

            user_json_path = f'{os.path.abspath(os.getcwd())}/Logs/json/{self.online["Username"]}.json'

            user_data = {"products": response['data']}

            with open(user_json_path, 'w') as json_file:
                json.dump(user_data, json_file, indent=2)

            print(f'Dados salvos em: {user_json_path}')
            
            for product in response['data']:
                for coluna, valor in product.items():
                    print(f'"{coluna}": "{valor}"')
            print()
        else:
            print("Nenhum product encontrado para este vendedor.")
        
        return response 
    #check
    def top_products_best_seller(self):
        response = self.supabase.table('products').select('productname', 'sales').order('sales', desc=True).execute()
        response = dict(response)
        if response:
            print("Ranking de products mais vendidos:")
            
            for product in response['data']:
                print("Nome do produto:", product['productname'], " Vendas:", product['sales'])
            print()
        else:
            print("Nenhum product encontrado.")
        
        return response
    
    #check
    def signup_new_product(self):
        self._verify_login()
        try:
            name = input("Digite o nome do novo produto: ")
            if not self._validate_product_name(name):
                print("Nome do produto inválido. Permitido apenas underline, acentos e ç.")
                return
            description = input("Digite o descrição do novo produto: ")
            price = float(input("Preço do product: "))
            category = input("Digite a categoria do novo produto: ")
            stock_quantity = random.randint(1,100);
            initial_stock_quantity = stock_quantity + random.randint(1,30)
            owneruserid = self.online['UserID']

            novo_product = {
                "productname": name,
                "description": description,
                "price": price,
                "stockquantity": stock_quantity,
                "initialstockquantity": initial_stock_quantity,
                "category": category,
                "owneruserid": owneruserid,
            }

            response = self.supabase.table('products').insert(novo_product).execute()
            print("product Inserido com sucesso: \n", response.json())
        except postgrest.exceptions.APIError as e:
            print(f"Erro ao comunicar-se com o sistema: {e}")
        except Exception as e2:
            print(f"Erro desconhecido: {e2}")

    def get_replenish_suggestion(self):
        self._verify_login()

        # Consultar products com estoque baixo considerando <= 10
        response = self.supabase.table('products').select('productname', 'sales').eq('owneruserid', self.online["UserID"]).lte('stockquantity', 10).execute()

        products = dict(response)
        low_stock_products = [product['productname'] for product in products['data']]
        if not low_stock_products:
            return "Não há produtos para serem reabastecidos no momento"
        prompt = f"Report which products are low in stock, for replenishing stock: {', '.join(low_stock_products)}"
        
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a assistant, skilled for recommending which products that have to replenish stock."},
            {"role": "user", "content": prompt}],
        )

        log_filename = f"{os.path.abspath(os.getcwd())}/Logs/openai/Reestock_logs/{self.online['Username']}_reestock_log.json"
        with open(log_filename, 'w') as log_file:
            log_data = {
                "username": self.online['Username'],
                "operation": "reestock_suggestion",
                "products": [
                    {"product_name": product['productname'], "message": completion.choices[0].message.content.strip()}
                    for product in products['data']
                ]
            }
            json.dump(log_data, log_file, indent=2)

        return completion.choices[0].message.content.strip()

    def get_suggestion_to_buy_new_products(self):
        self._verify_login()

        # Consultar products top5 mais vendidos
        response_ranking = self.supabase.table('products').select('productname', 'sales').order('sales', desc=True).limit(5).execute()
        products_ranking = dict(response_ranking)

        if not products_ranking or not products_ranking['data']:
            return "Não há products disponíveis para sugestão no momento!"

        top_selling_products = [product['productname'] for product in products_ranking['data']]

        prompt = f"Consider to sell newer products based in our best sellers: {', '.join(top_selling_products)}"
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant, skilled for recommending new products."},
                {"role": "user", "content": prompt}],
        )
        
        log_filename = f"{os.path.abspath(os.getcwd())}/Logs/openai/Top_sold_logs/{self.online['Username']}_top_sold.json"
        with open(log_filename, 'w') as log_file:
            log_data = {
                "username": self.online['Username'],
                "operation": "buy_suggestions",
                "products": [
                    {"product_name": product['productname'], "message": completion.choices[0].message.content.strip()}
                    for product in products_ranking['data']
                ]
            }
            json.dump(log_data, log_file, indent=2)

        return completion.choices[0].message.content.strip()
