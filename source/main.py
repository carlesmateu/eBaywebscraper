# main.py

import pandas as pd
from ebay_scraper import scrape_ebay
from config import ebay_filters
from filters import filter_forbidden_terms
from datetime import datetime  # Importar datetime para obtener la fecha actual

def main():
    url = "https://www.ebay.es/sch/i.html"
    params = {
        '_from': 'R40',
        '_nkw': 'pixel7pro',
        'LH_ItemCondition': ebay_filters["item_conditions"]["Used"],  # Condició de l'article; 'Usat'.
        'LH_PrefLoc': ebay_filters["item_locations"]["International"],  # Localització de l'article; Internacional.
        '_udlo': '200',  # Preu mínim.
        '_udhi': '400',  # Preu màxim.
        '_dcat': ebay_filters["directories"]["No Directory"],  # Filtrar per ID de directori.
        '_sacat': ebay_filters["categories"]["No Category"],  # Filtrar per ID de categoria.
        '_sop': ebay_filters["sort_order"]["Time: newly listed"],  # Ordenar per "Temps: recents".
        'LH_Sold': '1',  # Mostrar només els articles venuts.
        'LH_Complete': '1',  # Mostrar només les subhastes acabades.
        'LH_BIN': '0',  # Mostrar només subhastes amb "Buy It Now".
        'LH_Auction': '1',  # Mostrar només subhastes.
        'LH_BO': '0',  # Mostrar només llistats que accepten ofertes.
        'LH_FS': '0',  # Mostrar només llistats amb enviament gratuït.
        '_ipg': '240',  # Nombre d'articles per pàgina.
        'rt': 'nc'  # Tipus de resultat; 'nc' indica que no s'utilitza memòria cau.
    }

    # Número màxim de pàgines a raspar
    max_pages = 5  # Es pot ajustar aquest valor.

    # Raspar dades des d'eBay
    all_items = scrape_ebay(url, params, max_pages)

    # Convertir a DataFrame
    items_df = pd.DataFrame(all_items)

    # Añadir la fecha de consulta
    query_date = datetime.now().strftime('%Y-%m-%d')  # Formato de fecha 'YYYY-MM-DD'
    items_df['Query Date'] = query_date  # Añadir la nueva columna con la fecha de consulta

    # Definir termes prohibits amb un ordre modificat
    forbidden_terms = [
        'verizon',
        '256 GB',
        'damaged',
        'at&t',
        'locked',
        'mini',
        'boost',
        'metro',
        'cricket',
        '512 GB,',
        'parts',
        'read description',
        'refurbished'
    ]

    # Filtrar el DataFrame per excloure els termes prohibits
    filtered_df = filter_forbidden_terms(items_df, forbidden_terms)

    # Restablir l'índex del DataFrame filtrat
    filtered_df = filtered_df.reset_index(drop=True)

    # Desar el DataFrame filtrat en un fitxer CSV
    filtered_df.to_csv('pixel_7_pro_ebay_evolution_prices.csv', index=False)

    # Mostrar les primeres files del conjunt de dades
    print(filtered_df.head())

if __name__ == '__main__':
    main()
