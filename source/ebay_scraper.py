# ebay_scraper.py

import requests
from bs4 import BeautifulSoup
from tor_connection import send_request_with_tor
from config import ebay_filters
import time  # Importa el módulo time para agregar el delay

def parse_item_details(item):
    """ Parse and return the details of an individual eBay item """
    title = item.find('div', class_='s-item__title').text
    price = item.find('span', class_='s-item__price').text
    link = item.find('a', class_='s-item__link')['href'].split('?')[0]
    image_url = item.find('div', class_='s-item__image-wrapper image-treatment').find('img').get('src','No image URL')

    # Additional item info
    description = item.find('div', class_='s-item__description').text if item.find('div', class_='s-item__description') else 'No description available'
    seller = item.find('span', class_='s-item__seller-info-text').text.strip() if item.find('span', class_='s-item__seller-info-text') else 'Seller not found'
    location = item.find('span', class_='s-item__location').text if item.find('span', class_='s-item__location') else 'Location unavailable'
    bids = item.find('span', class_='s-item__bids').text if item.find('span', class_='s-item__bids') else '0 bids'
    time_left = item.find('span', class_='s-item__time-left').text if item.find('span', class_='s-item__time-left') else 'Time remaining unknown'
    seller_rating = item.find('div', class_='s-item__reviews').text if item.find('div', class_='s-item__reviews') else 'No reviews'
    shipping_info = item.find('span', class_='s-item__shipping').text if item.find('span', class_='s-item__shipping') else 'No shipping info provided'

    return {
        'Title': title,
        'Price': price,
        'Link': link,
        'Image URL': image_url,
        'Description': description,
        'Seller': seller,
        'Location': location,
        'Bids': bids,
        'Time Left': time_left,
        'Seller Rating': seller_rating,
        'Shipping Info': shipping_info
    }

def fetch_ebay_page(url, params, page_num):
    """ Fetch the HTML content of an eBay search results page """
    params['_pgn'] = page_num
    response = send_request_with_tor(url, params)
    
    # Añadir un retraso entre solicitudes
    time.sleep(2)  # Espera de 2 segundos entre cada solicitud (ajusta el valor según lo que necesites)

    return response.text

def is_last_page(html_content):
    """ Check if there is no 'next' button, indicating the last page """
    soup = BeautifulSoup(html_content, 'html.parser')
    next_button = soup.find('button', class_='pagination__next', type='next')
    return next_button and next_button.get('aria-disabled') == 'true'

def scrape_ebay(url, params, max_pages):
    """ Scrape eBay search results across multiple pages """
    all_items = []
    page_num = 1
    
    while page_num <= max_pages:
        print(f'Scraping page {page_num} of {max_pages}...')
        
        html_content = fetch_ebay_page(url, params, page_num)
        
        if is_last_page(html_content):
            print('Reached the last page. Stopping...')
            break

        # Extract item details from the current page
        soup = BeautifulSoup(html_content, 'html.parser')
        items = soup.find_all('div', class_='s-item__wrapper clearfix')[2:]  # Skip irrelevant first items
        
        for item in items:
            item_details = parse_item_details(item)
            all_items.append(item_details)

        page_num += 1

    return all_items
