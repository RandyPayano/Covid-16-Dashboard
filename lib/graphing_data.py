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


def hubei_age_data():
    """data for age graph"""
    data = pd.DataFrame([{
    "group": "0 to 9", "Confirmed cases": "416", "Deaths": "0", "Mortality": "0.00%"},
    {"group": "10 to 19", "Confirmed cases": "549", "Deaths": "1", "Mortality": "0.20%"},
    {"group": "20 to 29", "Confirmed cases": "3619", "Deaths": "7", "Mortality": "0.10%"},
    {"group": "30 to 39", "Confirmed cases": "7600", "Deaths": "18", "Mortality": "0.20%"},
    {"group": "40 to 49", "Confirmed cases": "8571", "Deaths": "38", "Mortality": "0.30%"},
    {"group": "50 to 59", "Confirmed cases": "10008", "Deaths": "130", "Mortality": "0.90%"},
    {"group": "60 to 69", "Confirmed cases": "8583", "Deaths": "309", "Mortality": "2.40%"},
    {"group": "70 to 79", "Confirmed cases": "3918", "Deaths": "312", "Mortality": "5.60%"},
    {"group": "80 and older", "Confirmed cases": "1408", "Deaths": "208", "Mortality": "11.10%"}])

    hubei_data_stacked = data.to_csv()

    return hubei_data_stacked



def hubei_preconditions_data():
    """data for pre-condition graph"""
    data = pd.DataFrame([{
                                        "group": "Missing Conditions", "Confirmed cases": "23690", "Deaths": "617", "Mortality": "1.90%"},
                                        {"group": "No Conditions", "Confirmed cases": "15536", "Deaths": "133", "Mortality": "0.50%"},
                                        {"group": "Hypertension", "Confirmed cases": "2683", "Deaths": "161", "Mortality": "3.80%"},
                                        {"group": "Diabetes", "Confirmed cases": "1102", "Deaths": "80", "Mortality": "4.50%"},
                                        {"group": "Respiratory disease", "Confirmed cases": "511", "Deaths": "32", "Mortality": "4.00%"},
                                        {"group": "Cardiovascular disease", "Confirmed cases": "873", "Deaths": "92", "Mortality": "6.80%"},
                                        {"group": "Cancer", "Confirmed cases": "107", "Deaths": "6", "Mortality": "3.60%"
                                         }])

    hubei_preconditions = data.to_csv()

    return hubei_preconditions