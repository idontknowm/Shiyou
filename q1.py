"""
Author: Yinqin Zhao
Date: 2024-2-27
Mail: zyq21@mails.tsinghua.edu.cn
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv


def get_all_tables(url):
    """
    Get all tables from the provided URL.

    Args:
    url (str): The URL to fetch tables from.

    Returns:
    list: List of tables found on the webpage.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        # Parse HTML content using Beautiful Soup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all tables on the page
        tables = soup.find_all('table')

        return tables

    except requests.RequestException as e:
        print("Request failed:", e)
        return None


def convert_table_to_list(table):
    """
    Convert a table into a list of lists.

    Args:
    table (BeautifulSoup): The BeautifulSoup object representing a table.

    Returns:
    list: List of lists representing the table data.
    """
    table_data = []
    rows = table.find_all('tr')
    for row in rows:
        row_data = []
        cells = row.find_all(['th', 'td'])
        for cell in cells:
            row_data.append(cell.get_text().strip())
        table_data.append(row_data)
    return table_data


def save_tables_as_csv(tables):
    """
    Save tables as CSV files.

    Args:
    tables (list): List of tables to be saved.
    """
    for i, table in enumerate(tables, start=1):
        table_data = convert_table_to_list(table)
        with open(f"table_{i}.csv", 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(table_data)
        print(f"Table {i} has been saved as table_{i}.csv")


def create_currency_dict(tables):
    """
    Create a dictionary mapping currency symbols to currency names.

    Args:
    tables (list): List of tables containing currency information.

    Returns:
    dict: Dictionary mapping currency symbols to currency names.
    """
    currency_dict = {}
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 5:
                currency_name = cols[1].text.strip()
                currency_symbol = cols[4].text.strip()
                currency_dict[currency_symbol] = currency_name
    return currency_dict


def find_currency_symbol(currency_name, currency_dict):
    """
    Find currency symbol based on currency name.

    Args:
    currency_name (str): The name of the currency.
    currency_dict (dict): Dictionary containing currency symbols and names.

    Returns:
    str: Currency symbol if found, otherwise a message indicating not found.
    """
    return currency_dict.get(currency_name, "Currency symbol not found")


# Variable to store all tables from different pages
all_tables = []


def get_price(start_date, end_date, currency):
    """
    Get the price of a currency for a given date range.

    Args:
    start_date (str): Start date of the range.
    end_date (str): End date of the range.
    currency (str): Currency name.

    Returns:
    str: Price of the currency.
    """
    url = 'https://srh.bankofchina.com/search/whpj/search_cn.jsp'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://srh.bankofchina.com/search/whpj/search_cn.jsp',
        'Origin': 'https://srh.bankofchina.com'
    }

    # Construct query parameters
    payload = {
        'erectDate': start_date,
        'nothing': end_date,
        'pjname': currency,
        'head': 'head_620.js',
        'bottom': 'bottom_591.js'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        html_content = response.text

        # Get the current page's content
        page_source = html_content
        # Parse the webpage content using Beautiful Soup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the specified table
        target_table = soup.find('table', {'cellpadding': '0', 'align': 'left', 'cellspacing': '0', 'width': '100%'})

        # If table found, add it to the list
        if target_table:
            all_tables.append(target_table)
        cols = target_table.find_all('td')
        print(cols[3].text.strip())
        # Output all page's table content to result.txt
        with open('result.txt', 'w') as f:
            for table in all_tables:
                f.write(str(table))
                f.write('\n\n')

    except requests.RequestException as e:
        print("Request failed:", e)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py start_date end_date currency_symbol")
        sys.exit(1)
    start_date = sys.argv[1]
    end_date = sys.argv[1]
    currency_symbol = sys.argv[2]
    currency = None

    url = 'https://www.11meigui.com/tools/currency'
    tables = get_all_tables(url)
    if tables:
        currency_dict = create_currency_dict(tables)
        currency = find_currency_symbol(currency_symbol, currency_dict)
    else:
        print("No tables found.")

    get_price(start_date, end_date, currency)
