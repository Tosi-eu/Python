from re import M
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import xlrd
from openpyxl import Workbook

Email_from = ""

msg = MIMEMultipart() #allows us to send emails

workbook = xlrd.open_workbook('C:/Users/Usuario/Desktop/Curso/WebScrapping/emails.xls')
sheet = workbook.sheet_by_name('Plan1')
rows = sheet.nrows
columns = sheet.ncols

msg['from'] = Email_from

# logs
Con = smtplib.SMTP('smtp.gmail.com', 587) #smtp is the server email, and 587 is the server gateaway
Con.starttls()
Con.login(Email_from, 'Guitosi12@')
msg['subject'] = "Parabéns pelo seu código em C"


#attach document
file_name = "gg.PNG"
attached = open(file_name, "rb")
base = MIMEBase('application', 'octet-stream') #it's the base, it's standard
base.set_payload((attached).read()) #reading file and saving him on computer memory
encoders.encode_base64(base) #codifying msg in base64
base.add_header('Content-Disposition', 'attachment; filename= %s'% (file_name)) #first and secod arguments are standard, file_name is variable
msg.attach(base) #attaching doc

for curr_row in range(0, rows):
    Email_to =  sheet.cell_value(curr_row, 0) #reading each cell in row
    msg['to'] = sheet.cell_value(curr_row, 0) #reading each cell in row


html = """
<html>
      <body>
            <p>Salve salve,<br>
            Como cê tá?<br>


            Vi seu código e achei legal, por que você não o posta no fórum??<br>

            <a href='https://forum.scriptbrasil.com.br/'>Clique aqui</a>
            para acessar o fórum do script brasil 8)<br>

            Até mais!
        </p>
    </body>
<html>

"""
msg_fix = MIMEText(html, "html")
msg.attach(msg_fix)
text = msg.as_string() # for avoiding that msg dont cointains anytihng different of strings
Con.sendmail(Email_from, Email_to, text)

Con.quit()
