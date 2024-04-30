import json
import random
import re
import markdown
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
        self.online = None
        self.error_message = None

    #check
    def sign_in(self, username, email):
        # Fazer login
        try:
            response = self.supabase.from_('users').select('*').eq('username', username).eq('email', email).execute()
        except postgrest.exceptions.APIError as e:
            self.error_message = f"Erro ao comunicar-se com o sistema (Supabase): {e}"
            return False
        except Exception as e:
            self.error_message = f"Erro desconhecido ao chamar a API do Supabase: {e}"
            return False

        try:
            if response:
                user_data = response.dict()
                self.online = {
                    "UserID": user_data['data'][0]['userid'],
                    "Username": user_data['data'][0]['username']
                }
                return True
            else:
                self.error_message = "Credenciais inválidas!"
                return False
        except IndexError:
            self.error_message = "Erro ao realizar a verificação do usuário. Credenciais inválidas!"
            return False
        
    #check
    def consult_informations(self):
        try:
            response = self.supabase.table('products').select('*').eq('owneruserid', self.online["UserID"]).execute()

            if response:
                print("Informações dos seus products:")
                response = dict(response)

                user_json_path = f'/home/guilherme/Desktop/Python/Gingalabs/flask/Logs/{self.online["Username"]}.json'

                user_data = {"products": response['data']}

                with open(user_json_path, 'w') as json_file:
                    json.dump(user_data, json_file, indent=2)

                print(f'Dados salvos em: {user_json_path}')
                
                for product in response['data']:
                    for coluna, valor in product.items():
                        print(f'"{coluna}": "{valor}"')
                print()
            else:
                print("Nenhum produto encontrado para este vendedor.")

        except postgrest.exceptions.APIError as e:
            print(f"Erro ao comunicar-se com o sistema (Supabase): {e}")
        except Exception as e:
            print(f"Erro desconhecido ao chamar a API do Supabase: {e}")
        
        return response 
    
    #check
    def top_products_best_seller(self):
        try:
            response = self.supabase.table('products').select('productname', 'sales').order('sales', desc=True).limit(10).execute()

            response = dict(response)
            if response:
                print("Ranking de products mais vendidos:")
                for product in response['data']:
                    print("Nome do produto:", product['productname'], " Vendas:", product['sales'])
                print()
            else:
                print("Nenhum product encontrado.")
            
            return response
        except postgrest.exceptions.APIError as e:
            print(f"Erro ao comunicar-se com o sistema (Supabase): {e}")
        except Exception as e:
            print(f"Erro desconhecido ao chamar a API do Supabase: {e}")

    # check
    def signup_new_product(self, name="", description="", price=0.0, category=""):
        try:
            stock_quantity = random.randint(1, 100)
            initial_stock_quantity = stock_quantity + random.randint(1, 30)
            owneruserid = self.online['UserID']

            # Check if price is None, set it to 0.0 if so
            if price is None:
                price = 0.0

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
            print(response)
        except postgrest.exceptions.APIError as e:
            print(e)
        except ValueError as e2:
            print(e2)
        except Exception as e3:
            print(e3)


    def get_replenish_suggestion(self):
        try:
            response = self.supabase.table('products').select('productname', 'sales').eq('owneruserid', self.online["UserID"]).lte('stockquantity', 10).execute()
            products = dict(response)
            low_stock_products = [product['productname'] for product in products['data']]
            
            if not low_stock_products:
                return "Não há produtos para serem reabastecidos no momento"
            
            # Formatar a lista de produtos como Markdown
            markdown_list = markdown.markdown('\n'.join(f'- {product}' for product in low_stock_products))
            
            prompt = f"Avise quais produtos estão com baixo estoque, para que o vendedor solcite reestoque:\n{markdown_list}"
        
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant, skilled for recommending which products need to replenish stock."},
                    {"role": "user", "content": prompt}
                ]
            )

            log_filename = f"/home/guilherme/Desktop/Python/Gingalabs/flask/Logs/reestock_Logs/{self.online['Username']}_reestock_log.json"
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

            return completion.choices[0].message.content.split('\n')
        except postgrest.exceptions.APIError as e:
            raise Exception(f"Erro ao comunicar-se com o sistema (Supabase): {e}")
        except Exception as e:
            raise Exception(f"Erro desconhecido ao chamar a API do Supabase: {e}")


    def get_suggestion_to_buy_new_products(self):
            # Consultar products top5 mais vendidos
            try:
                response_ranking = self.supabase.table('products').select('productname', 'sales').order('sales', desc=True).limit(5).execute()

                products_ranking = dict(response_ranking)

                if not products_ranking or not products_ranking['data']:
                    return "Não há produtos disponíveis para sugestão no momento!"

                top_selling_products = [product['productname'] for product in products_ranking['data']]

                prompt = f"Sugira novos produtos baseados na venda dos nossos mais vendidos: {', '.join(top_selling_products)}"
                
                completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an assistant, skilled for recommending new products."},
                        {"role": "user", "content": prompt}],
                )
                
                log_filename = f"/home/guilherme/Desktop/Python/Gingalabs/flask/Logs/new_product_logs//{self.online['Username']}_top_sold.json"
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

                return completion.choices[0].message.content.split('\n')
            except postgrest.exceptions.APIError as e:
                print(f"Erro ao comunicar-se com o sistema (Supabase): {e}")
            except Exception as e:
                print(f"Erro desconhecido ao chamar a API do Supabase: {e}")
