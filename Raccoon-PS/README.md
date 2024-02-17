# Raccoon-PS

Olá,

Aqui estarão explicadas cada pergunta e como pensei em realizar cada questão, logo:


1) Qual a média de gastos de pessoas com ingresso Pista?

  Nessa questão, minha idéia foi: juntarei a planilha 1 com a 2, e usarei condicionais, para verificar aqueles que efetivamente foram ao show e estavam na pista, e assim terei também como base gastos na mesma planilha, assim podendo aplicar .mean(), encontrando a média.


<div align="center">
    <img src="https://user-images.githubusercontent.com/87606621/173205548-6e993980-1ab1-4ab9-abde-5374f931042f.PNG" width="700px" /><br>
    <img src="https://user-images.githubusercontent.com/87606621/173205571-0b0f06c1-cbec-44fc-8cbe-b6bab2928bb0.PNG" width="300px" />
</div>

2)Quais pessoas não compareceram aos shows?

  Não houveram pessoas que não compareceram, uma vez que existem aqueles que, embora não tivessem feito compra efetiva de ingressos com a AT, há gastos, mesmo que mínimos, exaltados pela tabela psel-de-compras.
  
3) Quais pessoas compraram ingressos com concorrentes?
    
<div align="center">
    <img src="https://user-images.githubusercontent.com/87606621/173205839-1fcfb63a-7a9e-4d1b-81d2-795caad98541.PNG" width="200px" />
</div>
    
 4) Qual o dia com maior gasto?

    Pelo resultado apontado pelo programa, o dia com maior movimentação financeira foi o dia 1, visto pelo código e pelo gráfico
    
<div align="center">
    <img src="https://user-images.githubusercontent.com/87606621/173207474-28142840-74e7-4897-9c2d-562abf932935.PNG" width="400px" /><br>
    <img src="https://user-images.githubusercontent.com/87606621/173207638-4a845ba1-2e9e-4756-acf2-4b2149e29b81.PNG" width="600px" />
</div>

 5) Faça uma lista com os clientes que desistiram de comprar o ingresso com a AT, a soma do valor que foi gasto durante os shows e quais shows eles desistiram de
comprar. Usar para resposta o esquema abaixo:

  foram separados os clientes com status diferentes de concluido, para assim serem inseridos em listas, utilizando de list comprehension e lambda function (para os shows de cada um), após isso, foi criado um novo Dataframe com essas listas. Utilizou-se a função to_json() para estruturar o novo df e, assim, foi feito o print dos resultados.
