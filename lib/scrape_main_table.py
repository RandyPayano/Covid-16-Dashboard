import pandas as pd
import numpy as np
from flask import Flask, render_template
from flask import jsonify
from flask import Flask, render_template, redirect
import requests
from bs4 import BeautifulSoup
import lxml.html.clean 

def scrape_main_table(saveto_csv = True):
    """Scrapes main table from Worldometers
    and saves it into a csv (static/data/covid16_table.csv)
    unless you set param to False"""
    print("running scrape_main_table()")
    population_latlong = pd.read_csv('static/data/population_latlong.csv')
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36","X-Requested-With": "XMLHttpRequest"}
    url = 'https://www.worldometers.info/coronavirus' 
    r = requests.get(url, headers=header)
    HCE = BeautifulSoup(r.content, features="lxml")
    df = pd.read_html(lxml.html.clean.clean_html(str(HCE.find('table', id="main_table_countries_today"))).replace('\n', ''))[0]
    covid19_table = df.fillna('0')
    covid19_table.rename(columns = {'Country,Other':'Country', 'Serious,Critical':'Critical'},inplace = True) 
    covid19_table = covid19_table.apply(lambda x: x.replace(',',''))
    final_table = covid19_table.drop(columns='Population')
    final_table = final_table.merge(population_latlong, on='Country')
    final_table = final_table.drop(columns='Unnamed: 0')
    final_table.loc[:,'TotalRecovered'] = final_table['TotalRecovered'].apply(pd.to_numeric, errors='coerce')
    final_table.loc[:,'TotalDeaths'] = final_table['TotalDeaths'].apply(pd.to_numeric, errors='coerce')
    final_table.loc[:,'Population'] = final_table['Population'] * 1000
    final_table.loc[:,'PopulationAffected'] = final_table['TotalCases'] / final_table['Population'] *100
    final_table.loc[:,'Cases Recovered'] =  final_table['TotalRecovered'] / final_table['TotalCases'] * 100
    final_table.loc[:,'ActiveCases'] = final_table['ActiveCases'].apply(pd.to_numeric, errors='coerce')
    final_table.loc[:,'Cases Active'] =  final_table['ActiveCases'] / final_table['TotalCases'] * 100
    final_table.loc[:,'Mortality Rate'] =  final_table['TotalDeaths'] / final_table['TotalCases'] * 100
    final_table_lastrow = final_table.iloc[-1, :]
    final_table = final_table[final_table.Country != 'Total:']
    final_table.loc['Total:'] = final_table_lastrow
    if saveto_csv == True:
        final_table.to_csv('static/images/covid19_table.csv')
    return final_table