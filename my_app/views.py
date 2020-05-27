from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import re
from .models import Search
# Create your views here.
BASE_SEARCH_LINK = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={}&_sacat=0"

class Product:
    def __init__(self, title, price, image, link):
        self.title = title
        self.price = price
        self.image = image
        self.link = link

def index(request):
    searchToFrontEnd=''
    productList = list()
    error_message = None
    info_message = None
    if request.method == 'POST':
        search = request.POST.get('search_input').strip()
        if search != '':
            Search.objects.create(content=search)
            searchToFrontEnd = search
            search = search.replace(' ', '+').strip()
            response = (BASE_SEARCH_LINK.format(search))
            content = requests.get(response).text
            soup = BeautifulSoup(content, "lxml")
            listings = soup.find_all('li',{'class':'s-item'})
            for listing in listings:
                title = listing.find('h3')
                price = listing.find('span', attrs={'class':'s-item__price'})
                image = listing.find('img', attrs={'class':'s-item__image-img'})
                link = listing.find('a')
                if title:
                    if "New Listing" in title:
                        title = title.replace('New Listing', '')
                    product = Product(title=title.text, price=price.text, image=image['src'], link=link["href"])
                    productList.append(product)
        else:
            error_message = 'Please enter the search keywords.'
        if len(productList) == 0:
            info_message = f'Sorry there are no results for {searchToFrontEnd}'

        



    
    
    


    context = {
        'title':'Home',
        'productList':productList,
        'search':searchToFrontEnd,
        'error_message':error_message,
        'info_message':info_message,
    }
    return render(request, 'index.html', context)

    