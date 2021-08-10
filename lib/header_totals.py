import pandas as pd

## Define functions for header info

def total_cases(final_table):
    """Grabs total number of cases.
    Args:
        final_table (DataFrame): DataFrame scrapped using scrape_main_table()
    Returns: 
        total_cases_df (DataFrame): Dataframe containing total overall cases
    """
    # Reset index and grab length of table to index rows
    final_table = final_table.reset_index().iloc[:,1:]
    table_length = len(final_table)-1
    
    # Grab TotalCases
    total_cases_df = final_table.loc[table_length:,['TotalCases']]
    total_cases_df.rename(columns={"TotalCases": "Confirmed Cases"}, inplace=True)
    total_cases_df.set_index("Confirmed Cases", inplace=True)
    
    return total_cases_df

def new_cases(final_table):
    """Grabs number of new cases.
    Args:
        final_table (DataFrame): DataFrame scrapped using scrape_main_table()
    Returns: 
        new_cases_df (DataFrame): Dataframe containing new overall cases
    """
    # Reset index and grab length of table to index rows
    final_table = final_table.reset_index().iloc[:,1:]
    table_length = len(final_table)-1
    # Grab NewCases
    new_cases_df =  final_table.loc[table_length:,['NewCases']]
    new_cases_df = new_cases_df.rename(columns={"NewCases": "New Cases"}).set_index("New Cases")
    
    return new_cases_df

def total_deaths(final_table):
    """Grabs number of total deaths.
    Args:
        final_table (DataFrame): DataFrame scrapped using scrape_main_table()
    Returns: 
        total_deaths_df (DataFrame): Dataframe containing total deaths
    """
    # Reset index and grab length of table to index rows
    final_table = final_table.reset_index().iloc[:,1:]
    table_length = len(final_table)-1
    # Grab Total Deaths
    total_deaths_df = final_table.loc[table_length:,["TotalDeaths"]].astype(int)
    total_deaths_df = total_deaths_df.rename(columns={"TotalDeaths": "Total Deaths"})
    total_deaths_df.set_index('Total Deaths', inplace=True)
    return total_deaths_df


def new_cases(final_table):
    """Grabs number of new cases.
    Args:
        final_table (DataFrame): DataFrame scrapped using scrape_main_table()
    Returns: 
        new_cases_df (DataFrame): Dataframe containing new cases
    """
    # Reset index and grab length of table to index rows
    final_table = final_table.reset_index().iloc[:,1:]
    table_length = len(final_table)-1
    # Grab NewCases
    new_cases_df =  final_table.loc[table_length:,['NewCases']]
    new_cases_df = new_cases_df.rename(columns={"NewCases": "New Cases"}).set_index("New Cases")
    
    return new_cases_df

def new_deaths(final_table):
    """Grabs number of new deaths.
    Args:
        final_table (DataFrame): DataFrame scrapped using scrape_main_table()
    Returns: 
        new_deaths_df (DataFrame): Dataframe containing new deaths
    """
    # Reset index and grab length of table to index rows
    final_table = final_table.reset_index().iloc[:,1:]
    table_length = len(final_table)-1
    # Grab NewCases
    new_deaths_df = final_table.loc[table_length:,['NewDeaths']]
    new_deaths_df = new_deaths_df.rename(columns={"NewDeaths": "New Deaths"}).set_index("New Deaths")
    
    return new_deaths_df

def total_recovered(final_table):
    """Grabs number of cases recovered.
    Args:
        final_table (DataFrame): DataFrame scrapped using scrape_main_table()
    Returns: 
        total_recovered_df (DataFrame): Dataframe containing total cases recovered
    """
    # Reset index
    final_table = final_table.reset_index().iloc[:,1:]
    
    # Grab Total Recovered
    total_recovered_df = pd.DataFrame({"Cases Recovered": [final_table['Cases Recovered'].iloc[-1]]}).reset_index()
    return total_recovered_df

def active_cases(final_table):
    """Grabs number of active cases.
    Args:
        final_table (DataFrame): DataFrame scrapped using scrape_main_table()
    Returns: 
        active_cases_df (DataFrame): Dataframe containing number of active cases
    """
    # Reset index
    final_table = final_table.reset_index().iloc[:,1:]
    table_length = len(final_table)-1
    # Grab active cases
    active_cases_df =  final_table.loc[table_length:,["ActiveCases"]]#.astype(int)
    active_cases_df = active_cases_df.rename(columns={"ActiveCases": "Active Cases"}).set_index("Active Cases")
    
    return active_cases_df

def pop_affected(final_table):
    """Grabs number of new cases.
    Args:
        final_table (DataFrame): DataFrame scrapped using scrape_main_table()
    Returns: 
        pop_affected_df (DataFrame): Dataframe containing population perc affected.
    """
    # Reset index
    final_table = final_table.reset_index().iloc[:,1:]
    table_length = len(final_table)-1
    # Grab Percentage Recovered
    pop_affected_df = final_table.loc[table_length:,['PopulationAffected']].round(4).astype(str) + '%'
    pop_affected_df = pop_affected_df.rename(columns={"PopulationAffected": "Population Affected"}).set_index('Population Affected')

    return pop_affected_df


def pct_recovered(final_table):
    """Grabs number of new cases.
    Args:
        final_table (DataFrame): DataFrame scrapped using scrape_main_table()
    Returns: 
        pct_recovered_df (DataFrame): Dataframe containing pct cases recovered.
    """
    # Reset index
    final_table = final_table.reset_index().iloc[:,1:]
    table_length = len(final_table)-1
    # Grab Percentage Recovered
    pct_recovered_df = final_table.loc[table_length:,['Cases Recovered']].round(2).astype(str) + '%'
    pct_recovered_df = pct_recovered_df.set_index('Cases Recovered')
    return pct_recovered_df


def cases_active(final_table):
    """Grabs number of new cases.
    Args:
        final_table (DataFrame): DataFrame scrapped using scrape_main_table()
    Returns: 
        pct_active_df (DataFrame): Dataframe containing pct of active cases. 
    """
    # Reset index
    final_table = final_table.reset_index().iloc[:,1:]
    table_length = len(final_table)-1
    # Grab Percentage Active
    pct_active_df = final_table.loc[table_length:,['Cases Active']].round(2).astype(str) + '%'  
    pct_active_df = pct_active_df.set_index('Cases Active')
    return pct_active_df

def mortality_rate(final_table):
    """Grabs number of new cases.
    Args:
        final_table (DataFrame): DataFrame scrapped using scrape_main_table()
    Returns: 
        mortality_rate_df (DataFrame): Dataframe containing mortality rate.
    """
    # Reset index
    final_table = final_table.reset_index().iloc[:,1:]
    table_length = len(final_table)-1
    # Grab Percentage Active
    
    mortality_rate_df= final_table.loc[table_length:,['Mortality Rate']].round(2).astype(str) + '%'
    mortality_rate_df = mortality_rate_df.set_index('Mortality Rate')
    return mortality_rate_df