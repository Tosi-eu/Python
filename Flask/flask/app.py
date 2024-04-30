import random
from flask import Flask, jsonify, render_template, request, redirect, session, url_for
import postgrest
from sistema import Sistema
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_KEY")
sistema = Sistema()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        if sistema.sign_in(username, email):
            session['online'] = True 
            return redirect(url_for('produto'))
        else:
            error = sistema.error_message
            return render_template('login.html', error=error)

    # Check for error message from redirect
    error = request.args.get('error')
    return render_template('login.html', error=error)

@app.route('/produto')
def produto():
    if not sistema.online:
        return redirect(url_for('login', error='Usuário não autenticado. Faça o login para acessar a página de produtos.'))
    return render_template('produto.html')

@app.route('/consultar_produtos', methods=['POST'])
def consultar_produtos():
    if request.method == 'POST':
        if sistema.online:
            response = sistema.consult_informations()
            if response:
                return render_template('lista_produtos.html', produtos=response['data'])
            else:
                return jsonify({'message': 'Nenhum produto encontrado para este vendedor.'})
        else:
            return jsonify({'error': 'Usuário não autenticado'}), 401
    return render_template('produto.html')

@app.route('/top_products_best_seller', methods=['POST'])
def top_products_best_seller():
    if request.method == 'POST':
        if sistema.online:
            response = sistema.top_products_best_seller()
            if response:
                return render_template('top_produtos.html', produtos=response['data'])
            else:
                return jsonify({'message': 'Nenhum produto encontrado.'})
        else:
            return jsonify({'error': 'Usuário não autenticado'}), 401
    return render_template('produto.html')

@app.route('/inserir_produto', methods=['GET', 'POST'])
def inserir_produto():
    if request.method == 'POST':
        try:
            name = request.form.get("productname")
            description = request.form.get("description")
            price = float(request.form.get("price"))
            category = request.form.get("category")
            stock_quantity = random.randint(1, 100)
            initial_stock_quantity = stock_quantity + random.randint(1, 30)
            owneruserid = sistema.online['UserID']

            novo_product = {
                "productname": name,
                "description": description,
                "price": price,
                "stockquantity": stock_quantity,
                "initialstockquantity": initial_stock_quantity,
                "category": category,
                "owneruserid": owneruserid,
            }

            sistema.supabase.table('products').insert(novo_product).execute()
            return render_template('inserir_produto.html', success_message="Produto inserido com sucesso!")

        except postgrest.exceptions.APIError as e:
            error_message = f"Erro ao comunicar-se com o sistema: {e}"
        except ValueError as e2:
            error_message = f"Formato de dado inválido. Inserção bloqueada: {e2}"
        except TypeError as e3:
            error_message = ""

        return render_template('inserir_produto.html', error_message=error_message)

    return render_template('inserir_produto.html', error_message=None, success_message=None)

@app.route('/reabastecer_produto', methods=['GET'])
def reabastecer_produto():
    try:
        suggestion = sistema.get_replenish_suggestion()
        return render_template('replenish_suggestion.html', success_message=suggestion)
    except Exception as e:
        return render_template('replenish_suggestion.html', error_message=f"Erro: {e}")
    
@app.route('/sugerir_novos_prod', methods=['GET'])
def sugerir_novo_produto():
    try:
        suggestion = sistema.get_suggestion_to_buy_new_products()
        return render_template('product_suggestion.html', success_message=suggestion)
    except Exception as e:
        return render_template('product_suggestion.html', error_message=f"Erro: {e}")
    
if __name__ == '__main__':
    app.run(debug=True)
