import pandas as pd

def do_lat_long():
    lat_long = pd.read_csv('static/images/covid16_table.csv')
    lat_long.iloc[:,2:] = lat_long.iloc[:,2:]
    lat_long['TotalCases'] = lat_long['TotalCases'].apply(pd.to_numeric, errors='coerce')
    lat_long = lat_long.iloc[:-1,:]
    graphing_value = []
    
    for e in lat_long['TotalCases']:
    
        if e < 200:
            graphing_value.append(150)
        if e >= 200 and e < 1000:  
            graphing_value.append(200)
        if e >= 1000 and e < 2000:    
            graphing_value.append(300)
        if e >= 2000 and e < 4000:  
            graphing_value.append(400)
        if e >= 4000 and e < 10000:    
            graphing_value.append(500)
        if e >= 10000 and e < 20000:    
            graphing_value.append(600)    
        if e >= 20000 and e < 30000:    
            graphing_value.append(700)
        if e >= 30000 and e < 40000:    
            graphing_value.append(800)    
        if e >= 40000 and e < 80000:    
            graphing_value.append(900)
        if e >= 80000 and e < 220000:    
            graphing_value.append(1000)
        if e >= 220000 and e < 350000:    
            graphing_value.append(1150)    
        if e >= 350000 and e < 550000:    
            graphing_value.append(1300)    
        if e >= 550000:    
            graphing_value.append(1500)   
        
    lat_long['Total'] = graphing_value






    graphing_active = []
    
    for e in lat_long['ActiveCases']:
    
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
        
    lat_long['Active'] = graphing_active
 
 
    lat_long = lat_long.fillna(0.000000)
    lat_long = lat_long.replace('\W', '')
    lat_long = lat_long.transpose() 
    lat_long = lat_long.to_dict()
    lat_long = [value for value in lat_long.values()]
    
    return lat_long