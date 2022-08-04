# pylint: disable=missing-final-newline
# pylint: disable=unused-import- W0611
# pylint: disable=missing-module-docstring
# -*- coding: utf-8 -*-

#A4 size --> 210mm x 297mm

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

canva = canvas.Canvas('PdfTest.pdf', pagesize=A4) #--> A4 is a default value
canva.drawImage("fipe.png", 100, 345, width=400, height=300)
canva.save()
