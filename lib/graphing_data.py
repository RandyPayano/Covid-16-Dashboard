import pandas as pd

def graph_pop_affected(final_table):
    """Returns data for d3 graph of population affected

    Args:
        final_table (DataFrame): final_table (DataFrame): DataFrame scrapped using scrape_main_table()

    Returns:
        csv: containing data for pop affected graph
    """
    # Sort DataFrame and filter to top 25, then return as CSV
    sorted_popaffected = final_table.sort_values(by=['PopulationAffected'], ascending=False)
    sorted_popaffect_25 = sorted_popaffected.iloc[:25,:]
    sorted_popaffect_25_csv = sorted_popaffect_25.to_csv()
    
    return sorted_popaffect_25_csv 


def graph_mortality_rate(final_table):
    """Returns data for d3 graph of mortality rate
    Args:
        final_table (DataFrame): final_table (DataFrame): DataFrame scrapped using scrape_main_table()

    Returns:
        csv: containing data for mortality rate graph
    """
    # Sort DataFrame and filter to top 25, then return as CSV
    sorted_mortality_rate = final_table.iloc[:-1].sort_values(by=['Mortality Rate'], ascending=False)
    sorted_mortality_rate_25 = sorted_mortality_rate.iloc[:25,:]
    sorted_mortality_rate_25 = sorted_mortality_rate_25.rename(columns={"Mortality Rate": "MortalityRate"})
    sorted_mortality_rate_25 = sorted_mortality_rate_25.to_csv()
    return sorted_mortality_rate_25

def graph_sorted_totals(final_table):
    """gets sorted table for total cases
    Args:
        final_table (df): [description]

    Returns:
        df:  sorted df for total cases
    """
    sorted_totals = final_table.sort_values(by=['TotalCases'], ascending=False).fillna(0)
    sorted_totals.loc[:,'TotalDeaths'] = sorted_totals['TotalDeaths'].astype(int)
    sorted_totals = sorted_totals[['Country','TotalCases','TotalDeaths','ActiveCases']]
    sorted_totals = sorted_totals.rename(columns={"TotalCases": "Cases","TotalDeaths": "Deaths", "ActiveCases": "Active"})
    sorted_totals = sorted_totals.set_index('Country')

    return sorted_totals


def graph_sorted_newcases(final_table):
    """gets sorted table for new cases
    Args:
        final_table (df): [description]

    Returns:
        df:  sorted df for new cases
    """
    sorted_new_cases = final_table[["Country", "NewCases","NewDeaths"]].set_index("Country")
    sorted_new_cases = sorted_new_cases[sorted_new_cases["NewCases"] != '0']
    
    # Iterating over values to remove "+" sign and be able to sort
    sorting_values_list = []
    for i in sorted_new_cases.NewCases:
        if "," in str(i):
            sorting_values_list.append(i[1:].replace(',', ''))
        else:  
            sorting_values_list.append(i)
            
    sorted_new_cases["sorter_col"] = sorting_values_list
    sorted_new_cases["sorter_col"] = sorted_new_cases["sorter_col"].apply(pd.to_numeric)
    
    sorted_new_cases = sorted_new_cases.sort_values(by="sorter_col", ascending=False)
    sorted_new_cases = sorted_new_cases.rename(columns={'NewCases':"Cases", "NewDeaths": "Deaths"})
    sorted_new_cases.drop(columns=["sorter_col"],inplace=True)
  
    return sorted_new_cases


def geo_graphing_values(final_table):

    lat_long_values = final_table
    lat_long_values.iloc[:,2:] = lat_long_values.iloc[:,2:]
    lat_long_values.loc[:,'TotalCases'] = lat_long_values.loc[:,'TotalCases'].apply(pd.to_numeric, errors='coerce')
    lat_long_values = lat_long_values.iloc[:-1,:]
    graphing_value = []
    
    for e in lat_long_values['TotalCases']:
    
        if e < 2000:
            graphing_value.append(150)
        if e >= 2000 and e < 10000:  
            graphing_value.append(200)
        if e >= 10000 and e < 20000:    
            graphing_value.append(300)
        if e >= 20000 and e < 40000:  
            graphing_value.append(400)
        if e >= 40000 and e < 100000:    
            graphing_value.append(500)
        if e >= 100000 and e < 200000:    
            graphing_value.append(600)    
        if e >= 200000 and e < 300000:    
            graphing_value.append(700)
        if e >= 300000 and e < 400000:    
            graphing_value.append(800)    
        if e >= 400000 and e < 800000:    
            graphing_value.append(900)
        if e >= 800000 and e < 2200000:    
            graphing_value.append(1000)
        if e >= 2200000 and e < 3500000:    
            graphing_value.append(1150)    
        if e >= 3500000 and e < 5500000:      
            graphing_value.append(1300)    
        if e >= 5500000:    
            graphing_value.append(1500)   
        
    lat_long_values.loc[:,'Total'] = graphing_value


    graphing_active = []
    
    for e in lat_long_values['ActiveCases']:
    
        if e < 200:
            graphing_active.append(150)
        if e >= 200 and e < 1000:  
            graphing_active.append(200)
        if e >= 1000 and e < 2000:    
            graphing_active.append(300)
        if e >= 2000 and e < 4000:  
            graphing_active.append(400)
        if e >= 4000 and e < 10000:    
            graphing_active.append(500)
        if e >= 10000 and e < 20000:    
            graphing_active.append(600)    
        if e >= 20000 and e < 30000:    
            graphing_active.append(700)
        if e >= 30000 and e < 40000:    
            graphing_active.append(450)    
        if e >= 40000 and e < 80000:    
            graphing_active.append(600)
        if e >= 80000 and e < 220000:    
            graphing_active.append(700)
        if e >= 220000 and e < 350000:    
            graphing_active.append(800)    
        if e >= 350000 and e < 550000:    
            graphing_active.append(1300)    
        if e >= 550000:    
            graphing_active.append(1500)  
        
    lat_long_values.loc[:,'Active'] = graphing_active
    lat_long_values = lat_long_values.fillna(0.000000)
    lat_long_values = lat_long_values.replace('\W', '')
    lat_long_values = lat_long_values.transpose() 
    lat_long_values = lat_long_values.to_dict()
    lat_long_values = [value for value in lat_long_values.values()]
    
    return lat_long_values    




def graph_progression_line():
    """gets timeseries data from github
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    and wrangles it into d3 format.
    Args:
    Returns:
        csv:  d3 data
    """
    confirmed_data = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
    confirmed_data = confirmed_data.rename(columns = {"Country/Region": "Country"})
    confirmed_data = confirmed_data.drop(["Lat","Long"], axis = 1)
    confirmed_data = confirmed_data.iloc[:,1:]
    confirmed_data = confirmed_data.groupby('Country').sum()
    confirmed_data = confirmed_data.transpose()
    confirmed_data.rename(columns={'US':'USA', 
                                   'United Kingdom':'UK', 
                                   'Korea, South': 'S. Korea',
                                   'Taiwan*': 'Taiwan',
                                   'United Arab Emirates': 'UAE',
                                   "Cote d'Ivoire": 'Ivory Coast',
                                    'Saint Vincent and the Grenadines': 'St. Vincent Grenadines'
                                    }, inplace=True)
    
    confirmed_data = confirmed_data.reset_index()
    confirmed_data.rename(columns={'index':'time'}, inplace=True)
    confirmed_data.loc[:,'value'] = confirmed_data['USA'] / 1000
    confirmed_data.loc[:,'time']=pd.to_datetime(confirmed_data['time'])
    response =  confirmed_data.to_csv()
    return response