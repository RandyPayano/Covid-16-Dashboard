import requests


def get_dict_info(response, number = 1):
    """function to grab news info from api response
    Args:
        response (request Response): response from api request
        number (int, optional): article number to get. Defaults to 1.

    Returns:
        dictionary with source, title, url, image, date
    """
    try:
        
        article_contents = response['articles'][number]

        dict_to_return = {
                         'articlesource': article_contents['source']['name'], 
                         'title': article_contents['title'], 
                         'img_url':article_contents['url'], 
                         'articleimage': article_contents['image'], 
                         'articlewhen':article_contents['publishedAt']}
    except:
        
        dict_to_return = {
                         'articlesource': "API limit", 
                         'title': "API limit", 
                         'img_url': "API limit", 
                         'articleimage': "API limit", 
                         'articlewhen': "API limit"}
    return dict_to_return   



def grab_top_news():    
    """returns four dictionaries containing news
    Returns:
        returns four dictionaries containing news
    """
    url = "https://gnews.io/api/v4/search?q=covid19&q=virus&lang=eng&max=10&country=us&token=600b3d1dc712bdc6c8d047a65f55c843"
    r = requests.get(url)
    response = r.json()
    
    news_dictionary1= get_dict_info(response, number = 1)
    news_dictionary2= get_dict_info(response, number = 2)   
    news_dictionary3= get_dict_info(response, number = 3)
    news_dictionary4= get_dict_info(response, number = 4)

    return news_dictionary1, news_dictionary2, news_dictionary3, news_dictionary4

if __name__ == '__main__':
    grab_top_news()