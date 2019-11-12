# -*- coding: utf-8 -*-
#!/usr/bin/python

from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import calendar
import xlsxwriter
import json
import xmltodict
import sys


#Descobre o Dia da Semana
def is_third_friday(s):
    d = datetime.strptime(s, '%d/%m')
    return d.weekday() == 4

# Descobre o mẽs Capitaliza e passa para Portuguẽs
def get_month_name(month_no, locale):
    with calendar.TimeEncoding(locale) as encoding:
        s = calendar.month_name[month_no]
        if encoding is not None:
            s = s.decode(encoding)
        return s.capitalize()


def treat_date(date):
    tmp = date.split("-")
    return tmp[2] + "/" + tmp[1] 



def generate_spreadsheet():
    
    #Cria planilha e formata a celulas 
    wb = xlsxwriter.Workbook('SemanaOperativa.xlsx')
    cell_title = wb.add_format({'bold': True,'align':'center', 'border': 1})
    sub_cell_title = wb.add_format({'bold': True, 'color':'#FFFFF','bg_color':'193b4f', 'align':'center', 'border': 1})
    dados_body = wb.add_format({'align':'center', 'border': 1}) 


    #Dia atual  
    data_atual = date.today()
    data_fim = data_atual + relativedelta(months=+3)
    #data_fim = date.fromordinal(data_atual.toordinal()+ 90)


    #Mes atual 
    mes_inicial   = data_atual.month
    mes_intervalo1 = int((data_atual + relativedelta(months=+1)).strftime("%m"))
    mes_intervalo2 = int((data_atual + relativedelta(months=+2)).strftime("%m")) 
    mes_final    = data_fim.month 

    #Cria Abas e faz um merge nas celulas
    ws = wb.add_worksheet( calendar.month_abbr[mes_inicial] + ' a ' + calendar.month_abbr[mes_final])
    ws.merge_range('B1:E1', get_month_name(mes_inicial,   "pt_BR.UTF-8"), cell_title)
    ws.merge_range('F1:I1', get_month_name(mes_intervalo1,  "pt_BR.UTF-8"), cell_title)
    ws.merge_range('J1:M1', get_month_name(mes_intervalo2,  "pt_BR.UTF-8"), cell_title)
    ws.merge_range('N1:Q1', get_month_name(mes_final,  "pt_BR.UTF-8"), cell_title)
    ws.set_column('A:A', 15)

    #Faz Leitura do Xml Transforma em Json
    with open('baciasDiaria.xml') as arquivo:
        dado = xmltodict.parse(arquivo.read())
        dados = json.dumps(dado)
        dados_bacia = json.loads(dados)
        i = 2
        acumula_prec = 0
        #Usa o Enumerate como contador de posição
        for p, v in enumerate(dados_bacia['main']['bacias']['bacia']):
            ws.write(i+p, 0, v['regiao_nome'], sub_cell_title)
            j = 1
            for _p, _v in enumerate(v['dados']):
                prec = float(_v['precDiaria'])
                if int(_v['dataDiaria'].split('/')[1]) > mes_inicial - 1 or int(_v['dataDiaria'].split('/')[1]) < mes_final + 1:
                    acumula_prec += prec
                    if is_third_friday(_v['dataDiaria']):
                        ws.write(1, j, _v['dataDiaria'], sub_cell_title)
                        ws.write(i+p, j, round(acumula_prec, 2), dados_body)
                        acumula_prec = 0
                        j+=1
            


    
    wb.close()
#Execeuta a Funcao 
if __name__== "__main__":
    generate_spreadsheet()
