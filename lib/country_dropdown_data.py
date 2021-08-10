
import pandas as pd
def countries_dropdown_data(main_table):
    print("------------------")
    info_mongodbpairs = main_table
    info_mongodbpairs = info_mongodbpairs.iloc[:,1:].fillna('0')
    info_mongodbpairs = info_mongodbpairs.drop(columns=['lat', 'long'])

    info_mongodbpairs =info_mongodbpairs.rename(columns={"TotalCases": "Total Cases", "PopulationAffected": "Population Affected", "NewCases": "New Cases","NewDeaths": "New Deaths", "TotalRecovered": "Total Recovered","TotalDeaths": "Total Deaths", "ActiveCases": "Active Cases"})
    info_mongodbpairs['Population Affected'] = info_mongodbpairs['Population Affected'].round(3).astype(str) + '%'
    info_mongodbpairs['Mortality Rate'] = info_mongodbpairs['Mortality Rate'].round(2).astype(str) + '%'
    info_mongodbpairs['Cases Active'] = info_mongodbpairs['Cases Active'].round(2).astype(str) + '%'
    info_mongodbpairs['Cases Recovered'] = info_mongodbpairs['Cases Recovered'].round(2).astype(str) + '%'
    info_mongodbpairs['Population'] = (info_mongodbpairs['Population'] /1000000).round(1).astype(str) + 'M'

    info_mongodbpairs =info_mongodbpairs.rename(columns={"Population": "A) World Population","Population Affected": "A) World Population Affected",  "Total Cases": "Aa) Total Cases",  "Total Recovered": "D) Total Recovered", "Cases Recovered": "D) Percentage Recovered","Total Deaths":"G) Total Deaths", "Mortality Rate": "G) Mortality Rate", "Active Cases": "E) Active Cases","Cases Active": "E) Percentage Active", "Critical": "F) Critical Condition", "Critical": "G) Critical Condition"})

    info_mongodbpairs = info_mongodbpairs.round(3)
    info_mongodbpairs = info_mongodbpairs.drop(columns=['New Cases', 'New Deaths'])
    info_mongodbpairs =  info_mongodbpairs.sort_values(by="Country")

    info_mongodbpairs = info_mongodbpairs.transpose() 
    info_mongodbpairs = info_mongodbpairs.to_dict()
    list_of_dics = [value for value in info_mongodbpairs.values()]

    list_of_dics = sorted(list_of_dics, key=lambda k: k['Country']) 
    
    return list_of_dics