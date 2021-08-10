from flask import Flask, render_template
from flask import jsonify
from flask import Flask, render_template
from lib.country_dropdown_data import countries_dropdown_data
from lib.scrape_main_table import scrape_main_table
from lib.news import grab_top_news
from lib.header_totals import total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases, pop_affected, pct_recovered, cases_active, mortality_rate
from lib.graphing_data import graph_pop_affected, graph_mortality_rate, graph_sorted_totals, graph_sorted_newcases, geo_graphing_values, graph_progression_line

app = Flask(__name__, static_url_path='')
# home page
@app.route("/")
def home_page():
    global main_table
    # scrape data   
    main_table = scrape_main_table(saveto_csv=False)
    # assign scrapped data to functions
    sorted_totals_response = graph_sorted_totals(main_table).to_html() 
    sorted_newcases_response = graph_sorted_newcases(main_table).to_html() 
    totalcases_response = total_cases(main_table).to_html() 
    newdeaths_response = new_deaths(main_table).to_html()
    newcases_response = new_cases(main_table).to_html() 
    totaldeaths_response = total_deaths(main_table).to_html() 
    totalrecovered_response = total_recovered(main_table).to_html() 
    activecases_response = active_cases(main_table).to_html() 
    popaffected_response = pop_affected(main_table).to_html() 
    pctrecovered_response = pct_recovered(main_table).to_html() 
    pctactive_response = cases_active(main_table).to_html() 
    mortalityrate_response = mortality_rate(main_table).to_html()

    # Define variables with news data
    news_dictionary1, news_dictionary2, news_dictionary3, news_dictionary4 = grab_top_news()
    return render_template("index.html", 
                           dictionary1 = news_dictionary1,
                           dictionary2 = news_dictionary2,
                           dictionary3 = news_dictionary3, 
                           dictionary4 = news_dictionary4, 
                           sorted_totals = sorted_totals_response, 
                           sorted_newcases = sorted_newcases_response, 
                           totalcases = totalcases_response, 
                           newdeaths = newdeaths_response,
                           newcases = newcases_response, 
                           totaldeaths = totaldeaths_response, 
                           totalrecovered = totalrecovered_response, 
                           activecases = activecases_response, 
                           popaffected = popaffected_response, 
                           pctrecovered = pctrecovered_response, 
                           pctactive = pctactive_response, 
                           mortalityrate = mortalityrate_response
                           )

# Return list of countries in json file
@app.route('/names')
def namess():
    country_list_response = main_table['Country']
    list_of_countries = jsonify(list(country_list_response))
    
    return list_of_countries

# Return Geographical values to chart
@app.route('/geo_graphing_values')
def namesss():
    response = jsonify(geo_graphing_values(main_table))
    return response

# Return MetaData for specific sample
@app.route("/metadata/<sample>")
def sample_metadata(sample = "China"):
    country_dropdown_data = countries_dropdown_data(main_table)
    for dicte in country_dropdown_data:
        if dicte['Country'] == sample:
            dataDict = dicte

    return jsonify(dataDict)

# Return data for d3 graph population affected
@app.route('/pop_affected')
def pop_affected_d():
    response = graph_pop_affected(main_table)
    return response

# Return data for d3 graph mortality rate
@app.route('/mortality_rate')
def mortality_rate_d():
    response = graph_mortality_rate(main_table)
    return response

# Return data for d3 case progression line
@app.route('/cases_progres')
def cases_progres_d():
    response = graph_progression_line()
    
    return response


if __name__ == '__main__':
    app.run(debug=True)


