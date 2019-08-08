#!/usr/bin/python
# -*- coding: utf-8 -*-
#!/usr/bin/python

from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

import calendar
import locale
import xlsxwriter
import json
import xmltodict
import sys

import requests
import pandas as pd

#Descobre o Dia da Semana
def is_third_friday(s):
    d = datetime.strptime(s, '%d/%m')
    return d.weekday() == 4 


def treat_date(date):
    tmp = date.split("-")
    return tmp[2] + "/" + tmp[1] 



def generate_spreadsheet():
    
    #Cria planilha e formata a celulas 
    wb = xlsxwriter.Workbook('SemenaOperativa.xlsx')
    cell_title = wb.add_format({'bold': True, 'color':'yellow','bg_color':'193b4f', 'align':'center', 'border': 1})
    sub_cell_title = wb.add_format({'bold': True, 'color':'#FFFFF','bg_color':'193b4f', 'align':'center', 'border': 1})
    dados_body = wb.add_format({'align':'center', 'border': 1}) 

    #Dia atual
    data_atual = date.today()
    # data_fim = data_atual + relativedelta(months=3)
    
    #Mes atual 
   
    mes_inicial   = data_atual.month
    # mes_intervalo1 = (data_atual + relativedelta(months=1)).month
    # mes_intervalo2 = (data_atual + relativedelta(months=2)).month
    mes_final = data_fim.month 

    #Cria Abas e faz um merge nas celulas
    if  mes_final > mes_intervalo2:

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        ws = wb.add_worksheet(calendar.month_abbr[mes_inicial] + ' a ' + calendar.month_abbr[mes_final])

        ws.merge_range('B1:E1', mes_inicial, cell_title)
        ws.merge_range('F1:I1', mes_intervalo1, cell_title)
        ws.merge_range('J1:M1', mes_intervalo2, cell_title)
        ws.merge_range('N1:Q1', mes_final, cell_title)
        ws.set_column('A:A', 15)
    else:
        ws = wb.add_worksheet( calendar.month_abbr[mes_inicial] + ' a ' + calendar.month_abbr[mes_intervalo2])
        ws.merge_range('B1:E1', mes_inicial, cell_title)
        ws.merge_range('F1:I1', mes_intervalo1, cell_title)
        ws.merge_range('J1:M1', mes_intervalo2, cell_title)
        ws.set_column('A:A', 15)


    #Faz Leitura do Xml Transforma em Json
    with open('./baciasDiaria.xml') as arquivo:
        dado = xmltodict.parse(arquivo.read())

    dados = json.dumps(dado)
    dados_bacia = json.loads(dados)

    print(type(dados_bacia))
    i = 2
    acumula_prec = 0
    #Usa o Enumerate como contador de posição
    for p, v in enumerate(dados_bacia['main']['bacias']['bacia']):
        ws.write(i+p, 0, v['regiao_nome'], sub_cell_title)
        j = 1
        for _p, _v in enumerate(v['dados']):
            prec = float(_v['precDiaria'])
            
            if int(_v['dataDiaria'].split('/')[1]) > int(mes_inicial) -1 and int(_v['dataDiaria'].split('/')[1]) < int(mes_final) + 1:
                acumula_prec += prec 
                if is_third_friday(_v['dataDiaria']):
                    ws.write(1, j, _v['dataDiaria'], sub_cell_title)
                    ws.write(i+p, j, round(acumula_prec, 2), sub_cell_title)
                    acumula_prec = 0
                    j+=1
        

def observed_api():
    api_path = 'http://172.20.14.200:8082/caterpie'
    fonte = 'reserv'
    station_data = requests.get(f'{api_path}/reserv_stations').json()['locations']
    yesterday_date = datetime.utcnow() - relativedelta(days=-1) 
    final_date = yesterday_date - relativedelta(months=3) 
    
    # print(station_data)
    for station in station_data.keys():
        print(station)
        station_timeseries_endpoint = '{}/{}/{}?freq=daily&initi_date={}&final_date={}'.format(api_path, fonte, station, yesterday_date.strftime('%Y-%m-%d'), final_date.strftime('%Y-%m-%d'))
        station_timeseries = requests.get(station_timeseries_endpoint).json()
        print (station_timeseries, station_timeseries_endpoint)
        break
        # Not working cause Observed data is not useful right now

def xml2dataframe(xml_file):
    '''
    From a xml JSON like file, return a pandas DATAFRAME
    the source file come from <place> and the subject is weekly basin data
    '''
    
    # Open xml file and make a JSON
    with open(xml_file) as arquivo:
        xml_data = xmltodict.parse(arquivo.read())        
    str_data = json.dumps(xml_data)
    json_data = json.loads(str_data)

    # Iterate over JSON adn make a DATAFRAME
    # The rolling date resets for every new Basin. It admits the data is daily and it starts after the update date
    # Might be useful to use the labeled data to confirme this date
    data_list = []
    file_update = datetime.strptime(json_data['main']['bacias']['atualizacao'], '%d-%m-%Y %H:%M:%S')
    for basin in json_data['main']['bacias']['bacia']:
        rolling_date = file_update
        for data in basin['dados']:
            rolling_date = rolling_date + relativedelta(days=1)
            data['bacia'] = basin['regiao_nome']
            data['date'] = rolling_date
            data_list.append(data)
    
    basin_df = pd.DataFrame(data_list)
    basin_df.set_index('date',inplace=True)
    return basin_df

def make_semana_operativa(df):
    '''
    From a DATAFRAME daily data, return a weekly DATAFRAME regarding the forecast for basins
    '''

    # make a column with the sum of 7 days data
    df.reset_index(inplace=True)
    df['soma7Dias'] = df['precDiaria'].rolling(window=7).sum()
    # print(df.head(10))
    

    # filter data only for Saturdays (new Operational Week)
    semana_operativa = df[:][df['date'].dt.dayofweek==5]
    semana_operativa.set_index('date',inplace=True)

    # if there are less than 7 days on the sum, it returns a NaN, therefore isn't a forecast only data
    semana_operativa.dropna(inplace=True)
    # print (semana_operativa.head(8))
    return semana_operativa


def make_xlsx(df):
    '''
    Creates a crude xlsx with all the data on the right places
    '''
    # Creates start and end dates based on the next 3 months
    today_date = datetime.utcnow() 
    final_date = today_date + relativedelta(months=3)
    last_day_of_month = calendar.monthrange(final_date.year, final_date.month)[1]
    final_date = final_date.replace(day=last_day_of_month)

    # Make the filter of the dataframe
    start_date = today_date.strftime('%Y-%m-%d')
    end_date = final_date.strftime('%Y-%m-%d')

    df = df.loc[start_date:end_date]

    # Group all data (Basins and months) in order to make a prettier output. Round numbers and remove ugly cells
    df.reset_index(inplace=True)
    df['mes'] = df['date'].dt.month
    grouped = df.groupby(['bacia', 'mes', 'dataDiaria'])['soma7Dias'].first()
    grouped = grouped.round(2)
    grouped.rename_axis(index={'bacia': '', 'mes': '', 'dataDiaria': ''}, inplace=True)

    # Transpose the data and save the file.
    grouped_t = grouped.unstack(level=[1, 2])


    writer = pd.ExcelWriter('SemanaOperativa/output.xlsx', engine ='xlsxwriter')

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    sheet_name = '{} a {}'.format(today_date.strftime('%b'), final_date.strftime('%b'))
    grouped_t.to_excel(writer, sheet_name=sheet_name)
    wb = writer.book
    ws = writer.sheets[sheet_name]

    cell_title = wb.add_format({'bold': True, 'color':'yellow','bg_color':'193b4f', 'align':'center', 'border': 1})
    sub_cell_title = wb.add_format({'bold': True, 'color':'#FFFFF','bg_color':'193b4f', 'align':'center', 'border': 1})
    dados_body = wb.add_format({'align':'center', 'border': 1}) 

    ws.write('A:A',sub_cell_title)
    writer.save()
    
    #h tps://xlsxwriter.readthedocs.io/working_with_conditional_formats.html
    # print(grouped_t)

def change_sheet_design(xls_file):
    pass

    # # Cria planilha e formata a celulas 
    # wb = xlsxwriter.Workbook('SemenaOperativa_2.xlsx')
    # cell_title = wb.add_format({'bold': True, 'color':'yellow','bg_color':'193b4f', 'align':'center', 'border': 1})
    # sub_cell_title = wb.add_format({'bold': True, 'color':'#FFFFF','bg_color':'193b4f', 'align':'center', 'border': 1})
    # dados_body = wb.add_format({'align':'center', 'border': 1}) 

    # locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    # ws = wb.add_worksheet('{} a {}'.format(start_date.strftime('%b'), end_date.strftime('%b')))

    # alphabet = ['ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        
#Execeuta a Funcao 
if __name__== "__main__":
    # generate_spreadsheet()
    file_path = 'SemanaOperativa/baciasDiaria.xml'
    df = xml2dataframe(file_path)
    so = make_semana_operativa(df)
    make_xlsx(so)



    # make_xlsx(so, today_date, final_date)