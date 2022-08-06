from ctypes import alignment
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

doc = SimpleDocTemplate("ProcessoSeletivo.pdf",
                        pagesize=A4,
                        rightMargin=72,
                        leftMargin=72,
                        topMargin=40,
                        bottomMargin=18)

Story=[]
ChartImage = "fipe.png"

StyleSheet = getSampleStyleSheet()
StyleSheet.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

StylesheetTitle = StyleSheet['Heading1']
StylesheetTitle.alignment = 1 # --> centrizar mensagem
LocationProd = Paragraph("DNA Consult - Processo Seletivo", StylesheetTitle)
Story.append(LocationProd)
Story.append(Spacer(1, 30))

ImageProportions = Image(ChartImage, 6*inch, 4*inch)
Story.append(ImageProportions)
Story.append(Spacer(1, 20))

Text = 'Caro leitor/avaliador da DNA Consult:'
Story.append(Paragraph(Text, StyleSheet["Justify"]))       
Story.append(Spacer(1, 20))

Text = 'Segue a breve explicação da tabela <b> FIPEZAP </b>, responsável por mostrar o preço dos imóveis em um período:'
Story.append(Paragraph(Text, StyleSheet["Justify"]))
Story.append(Spacer(1, 12))

Text = '&nbsp O preço de venda dos imóveis residenciais registrou um aumento de 0,48% em abril \
          segundo o Índice FipeZap divulgado nesta quarta-feira (4). No mês anterior, o avanço foi de 0,55%.A alta apurada \
        pelo Índice FipeZap deve ficar abaixo do avanço projetado para o Índice Nacional de Preços ao Consumidor Amplo (IPCA). \
          Segundo o boletim Focus, do Banco Central, a inflação deve ter subido 0,95% no mês passado.<BR/>\
          &nbsp Nos primeiros quatro meses do ano, os preços dos imóveis residenciais avançaram 2,07%, também abaixo da inflação esperada para o período (4,18%). \
          Em abril, 13 das 16 capitais monitoradas pelo Índice FipeZap tiveram alta no preço médio de venda dos imóveis. \
          As principais foram Goiânia (+1,51%), João Pessoa (+1,48%), Vitória (+1,37%), Curitiba (+1,29%) e Recife (+1,25%). \
          As que registraram queda, por sua vez, foram Manaus (-1,33%), Brasília (-0,84%) e Maceió (-0,09%). \
          No acumulado em 12 meses, o Índice FipeZap tem alta de 6,29%, enquanto a expectativa para a inflação é de 12,01%. <BR/>\
          &nbsp Na Análise do último mês o Índice FipeZAP+, que acompanha o comportamento dos preços de venda de imóveis residenciais em 50 cidades brasileiras, \
          acabou por registrar uma alta de 0,49% em fevereiro em 2022, após avançar 0,53% no mês anterior, o que implica dizer que esse mercado continua em alta.'

Story.append(Paragraph(Text, StyleSheet["Justify"]))
Story.append(Spacer(1, 40))

Text = 'Agradeço por estar tendo essa oportunidade de mostrar meu trabalho, <BR/><BR/> \
        <b> Guilherme Tosi </b>'
Story.append(Paragraph(Text, StyleSheet["Justify"]))
Story.append(Spacer(1, 40))

StylesheetTitle = StyleSheet['Normal']
StylesheetTitle.alignment = 1
LocationProd = Paragraph("<strong> São Carlos/SP, 5 de Outubro de 2022 </strong>", StylesheetTitle) 
Story.append(LocationProd)

doc.build(Story)
