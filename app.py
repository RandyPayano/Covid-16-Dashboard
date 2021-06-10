
import pandas as pd
import numpy as np
from flask import Flask, render_template
from flask import jsonify
from flask import Flask, render_template, redirect
import requests
from bs4 import BeautifulSoup
from latty import do_lat_long
from dictie import dict_list

app = Flask(__name__, static_url_path='')

population_latlong = pd.read_csv('population_latlong.csv')
header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36","X-Requested-With": "XMLHttpRequest"}
url = 'https://www.worldometers.info/coronavirus' 
r = requests.get(url, headers=header)
HCE = BeautifulSoup(r.content)
import lxml.html.clean 
df = pd.read_html(lxml.html.clean.clean_html(str(HCE.find('table', id="main_table_countries_today"))).replace('\n', ''))[0]
covid16_table = df.fillna('0')
covid16_table.rename(columns = {'Country,Other':'Country', 'Serious,Critical':'Critical'},inplace = True) 
covid16_table = covid16_table.apply(lambda x: x.replace(',',''))
final_table = covid16_table
final_table = final_table.drop(columns='Population')


final_table = final_table.merge(population_latlong, on='Country')
final_table = final_table.drop(columns='Unnamed: 0')


final_table['TotalRecovered'] = final_table['TotalRecovered'].apply(pd.to_numeric, errors='coerce')
final_table['TotalDeaths'] = final_table['TotalDeaths'].apply(pd.to_numeric, errors='coerce')
final_table['Population'] = final_table['Population'] * 1000
final_table['PopulationAffected'] = final_table['TotalCases'] / final_table['Population'] *100
final_table['Cases Recovered'] =  final_table['TotalRecovered'] / final_table['TotalCases'] * 100

final_table['ActiveCases'] = final_table['ActiveCases'].apply(pd.to_numeric, errors='coerce')
final_table['Cases Active'] =  final_table['ActiveCases'] / final_table['TotalCases'] * 100
final_table['Mortality Rate'] =  final_table['TotalDeaths'] / final_table['TotalCases'] * 100


final_table_lastrow = final_table.iloc[-1, :]
final_table = final_table[final_table.Country != 'Total:']
final_table.loc['Total:'] = final_table_lastrow


final_table.to_csv('static/images/covid16_table.csv')


sorted_totals = final_table.sort_values(by=['TotalCases'], ascending=False)
sorted_totals['TotalDeaths'] = sorted_totals['TotalDeaths'].astype(int)
sorted_totals  = sorted_totals.iloc[1:].fillna(0)
sorted_totals  =sorted_totals[['Country','TotalCases','TotalDeaths','ActiveCases']]
sorted_totals  = sorted_totals.rename(columns={"TotalCases": "Cases","TotalDeaths": "Deaths", "ActiveCases": "Active"})
sorted_totals = sorted_totals.set_index('Country')

sorted_popaffectcsv = final_table.sort_values(by=['PopulationAffected'], ascending=False)
sorted_popaffectcsv = sorted_popaffectcsv.iloc[:25,:]
print(sorted_popaffectcsv)
sorted_popaffectcsv.to_csv('static/images/sorted_popaffectcsv.csv')

sorted_mortalityratecsv = final_table.iloc[:-1].sort_values(by=['Mortality Rate'], ascending=False)

sorted_mortalityratecsv = sorted_mortalityratecsv.iloc[:25,:]
sorted_mortalityratecsv = sorted_mortalityratecsv.rename(columns={"Mortality Rate": "MortalityRate"})
sorted_mortalityratecsv.to_csv('static/images/sorted_mortalityratecsv.csv')


@app.route("/")
def home_page():
    # GET SORTED NEW CASES AND DEATHS

    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36","X-Requested-With": "XMLHttpRequest"}
    url = 'https://www.worldometers.info/coronavirus' 
    r = requests.get(url, headers=header)
    HCE = BeautifulSoup(r.content)
    import lxml.html.clean 
    df = pd.read_html(lxml.html.clean.clean_html(str(HCE.find('table', id="main_table_countries_today"))).replace('\n', ''))[0]
    covid16_table = df.fillna('0')
    covid16_table.rename(columns = {'Country,Other':'Country', 'Serious,Critical':'Critical'},inplace = True) 
    covid16_table = covid16_table.apply(lambda x: x.replace(',',''))
    final_table = covid16_table
    totals = final_table.iloc[-1,:].values[1:]
    final_table = final_table.iloc[:,1:]
    final_table = final_table[final_table['Country'] != 'Total:']
    final_table.loc['Total'] = totals


    startswithlist = []

    for i in covid16_table.NewCases:
        if "," in str(i):
            startswithlist.append(i[1:].replace(',', ''))
            
        else:
         
            startswithlist.append(i)


    covid16_table['sortingnewcases'] = startswithlist
    covid16_table['sortingnewcases'] = covid16_table['sortingnewcases'].apply(pd.to_numeric)
    sorted_newcases = covid16_table[covid16_table['sortingnewcases'] > 0 ]
    sorted_newcases = sorted_newcases.sort_values(by=['sortingnewcases'], ascending=False)

    sorted_newcases = sorted_newcases.set_index('Country')
    sorted_newcases = sorted_newcases[['NewCases', 'NewDeaths']].fillna(0)
    sorted_newcases = sorted_newcases.rename(columns={'NewCases':"Cases", "NewDeaths": "Deaths"})
    sorted_newcases = sorted_newcases.iloc[:,:]
  


    final_table = pd.read_csv('static/images/covid16_table.csv')
    final_table = final_table.iloc[:,1:]
   
    lengthy = len(final_table)-1
    #TotalCases
    totalcases = final_table.loc[lengthy:,['TotalCases']]
    totalcases.rename(columns={"TotalCases": "Confirmed Cases"}, inplace=True)
    totalcases.set_index("Confirmed Cases", inplace=True)
    
 

    #NewCases
    newcases =  final_table.loc[lengthy:,['NewCases']]
  
    newcases = newcases.rename(columns={"NewCases": "New Cases"}).set_index("New Cases")
    
    #TotalDeaths
    totaldeaths = final_table.loc[lengthy:,["TotalDeaths"]].astype(int)
    totaldeaths = totaldeaths.rename(columns={"TotalDeaths": "Total Deaths"})
    totaldeaths.set_index('Total Deaths', inplace=True)
   
    #NewDeaths
    newdeaths = final_table.loc[lengthy:,['NewDeaths']].set_index("NewDeaths")
   
    newdeaths = newdeaths.rename(columns={"NewDeaths": "New   Deaths"})
    #Totalrecovered
    totalrecovered= pd.DataFrame({"Cases Recovered": [final_table['Cases Recovered'].iloc[-1]]}).reset_index()
    
    
    #totalrecovered = totalrecovered.set_index('TotalRecovered')
    #Activecases
    activecases =  final_table.iloc[-1:,6:7]
   
    #Pop % Affected
  
    popaffected = final_table.loc[lengthy:,['PopulationAffected']].round(4).astype(str) + '%'
 
    popaffected = popaffected.rename(columns={"PopulationAffected": "Population Affected"}).set_index('Population Affected')


    #Percentage Recovered
    pctrecovered = final_table.loc[lengthy:,['Cases Recovered']].round(2).astype(str) + '%'
    pctrecovered = pctrecovered.set_index('Cases Recovered')



    #Percentage Active
    pctactive = final_table.loc[lengthy:,['Cases Active']].round(2).astype(str) + '%'
    pctactive = pctactive.set_index('Cases Active')
   #Mortality Rate %
    mortalityrate= final_table.loc[lengthy:,['Mortality Rate']].round(2).astype(str) + '%'
    mortalityrate = mortalityrate.set_index('Mortality Rate')
   
    # NEWSSSSSSSSSSSSSSSSSSSSSSSSSS

    from datetime import date, timedelta
    today = date.today()
    from_date = today - timedelta(days = 8)
    page = requests.get(f'http://newsapi.org/v2/everything?q=Corona?Virus&from={from_date}&sortBy=publishedAt&apiKey=71788d9278894c70987a0a2d0e8c6120')
    page = page.json()


    articlesource = []
    articletitle = []
    articleimage = []
    articlewhen = []
    articleurl = []
    for e in range(4):
        articlesource.append(page['articles'][e]['source']['name'])
        articletitle.append(page['articles'][e]['title'])
        articleurl.append(page['articles'][e]['url'])
        articleimage.append(page['articles'][e]['urlToImage'])
        articlewhen.append(page['articles'][e]['publishedAt'])
        
    dictionary1= {'articlesource': articlesource[0], 'title': articletitle[0], 'img_url':articleurl[0], 'articleimage': articleimage[0], 'articlewhen':articlewhen[0] }
    dictionary2= {'articlesource': articlesource[1], 'title': articletitle[1], 'img_url':articleurl[1], 'articleimage': articleimage[1], 'articlewhen':articlewhen[1] }    
    dictionary3= {'articlesource': articlesource[2], 'title': articletitle[2], 'img_url':articleurl[2], 'articleimage': articleimage[2], 'articlewhen':articlewhen[2] }
    dictionary4= {'articlesource': articlesource[3], 'title': articletitle[3], 'img_url':articleurl[3], 'articleimage': articleimage[3], 'articlewhen':articlewhen[3] }


    mydictlisty = [dictionary1,dictionary2]
    return render_template("index.html", mydictlisty = mydictlisty, dictionary1 = dictionary1, dictionary2= dictionary2,dictionary3= dictionary3, dictionary4= dictionary4, sorted_totals =sorted_totals.to_html(), sorted_newcases = sorted_newcases.to_html(), totalcases = totalcases.to_html(), newdeaths = newdeaths.to_html(),newcases=newcases.to_html(), totaldeaths=totaldeaths.to_html(), totalrecovered = totalrecovered.to_html(), activecases = activecases.to_html(), popaffected = popaffected.to_html(), pctrecovered = pctrecovered.to_html(), pctactive = pctactive.to_html(), mortalityrate = mortalityrate.to_html())


@app.route('/names')
def namess():

    list_countries = pd.read_csv('static/images/covid16_table.csv')
    return jsonify(list(list_countries['Country']))


@app.route('/latandlong')
def namesss():
    return jsonify(do_lat_long())

# Return MetaData for specific sample
@app.route("/metadata/<sample>")
def sample_metadata(sample = "China"):
    
    for dicte in dict_list():
        if dicte['Country'] == sample:
            dataDict = dicte

    return jsonify(dataDict)

if __name__ == '__main__':
    app.run(debug=True)


