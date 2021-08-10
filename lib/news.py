import requests
def grab_top_news():
    """Uses newsAPI to grab top news related to Covid-19
    Returns:
        dictionaries: 4 dictionaries containing news headers
    """
    from datetime import date, timedelta
    today = date.today()
    from_date = today - timedelta(days = 18)
    page = requests.get(f'http://newsapi.org/v2/everything?q=Covid&from={from_date}&sortBy=populrity&apiKey=71788d9278894c70987a0a2d0e8c6120')
    page = page.json()

    articlesource = []
    articletitle = []
    articleimage = []
    articlewhen = []
    articleurl = []
    
    counter = 0
    article_number = 0
    while article_number < 4:
        
        if ".jpg" in page['articles'][counter]['urlToImage']:
        
            articlesource.append(page['articles'][counter]['source']['name'])
            articletitle.append(page['articles'][counter]['title'])
            articleurl.append(page['articles'][counter]['url'])
            articleimage.append(page['articles'][counter]['urlToImage'])
            articlewhen.append(page['articles'][counter]['publishedAt'])
            
            article_number += 1
            counter += 1
        else:
            counter += 1
            pass 
            
    news_dictionary1= {'articlesource': articlesource[0], 'title': articletitle[0], 'img_url':articleurl[0], 'articleimage': articleimage[0], 'articlewhen':articlewhen[0] }
    news_dictionary2= {'articlesource': articlesource[1], 'title': articletitle[1], 'img_url':articleurl[1], 'articleimage': articleimage[1], 'articlewhen':articlewhen[1] }    
    news_dictionary3= {'articlesource': articlesource[2], 'title': articletitle[2], 'img_url':articleurl[2], 'articleimage': articleimage[2], 'articlewhen':articlewhen[2] }
    news_dictionary4= {'articlesource': articlesource[3], 'title': articletitle[3], 'img_url':articleurl[3], 'articleimage': articleimage[3], 'articlewhen':articlewhen[3] }

    return news_dictionary1, news_dictionary2, news_dictionary3, news_dictionary4
