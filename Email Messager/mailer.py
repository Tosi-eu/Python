from re import M
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import xlrd
from openpyxl import Workbook

Email_from = "" #email root (yours, probably :P)

msg = MIMEMultipart() #allows us to send emails

workbook = xlrd.open_workbook('C:/Users/Usuario/Desktop/Curso/WebScrapping/emails.xls') #this is my directory path, erase it and put yours 
sheet = workbook.sheet_by_name('') # function's name explains all

rows = sheet.nrows
columns = sheet.ncols
msg['from'] = Email_from

# logs
Con = smtplib.SMTP('smtp.gmail.com', 587) #smtp is the server email, and 587 is the server gateaway
Con.starttls()
Con.login(Email_from, '')
msg['subject'] = "" #any subject different of physics


#attach document
file_name = "" #docx, pdf, png, jpeg, xlsx
attached = open(file_name, "rb")
base = MIMEBase('application', 'octet-stream') #it's standard, don't modify
base.set_payload((attached).read()) #reading file sent in 'file_name'
encoders.encode_base64(base)
base.add_header('Content-Disposition', 'attachment; filename= %s'% (file_name)) #first and secod arguments are standard, file_name is variable
msg.attach(base)

for curr_row in range(0, rows): #basically, sheet will be read, and each email in sheet[row][column] eill be selected
    Email_to =  sheet.cell_value(curr_row, 0) 
    msg['to'] = sheet.cell_value(curr_row, 0) 
    
html = """
<html>
      <body>
            <p>Salve salve,<br><br>
            Como cê tá?<br><br>


            Vi seu código e achei legal, por que você não o posta no fórum??<br>

            <a href='https://forum.scriptbrasil.com.br/'>Clique aqui</a>
            para acessar o fórum do script brasil 8)<br><br>

            Até mais!
        </p>
    </body>
<html>

"""
msg_fix = MIMEText(html, "html")
msg.attach(msg_fix)
text = msg.as_string()
Con.sendmail(Email_from, Email_to, text)

Con.quit()
