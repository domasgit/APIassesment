from secrets import baseurl, estab, key, secret
import requests, json

headers		= {
	'Content-Type'			: 'application/json',
	'Accept'				: 'application/json',
	'API-AUTHENTICATION'	: key + ':' + secret
}

def get_menu():
    url = f"{baseurl}/weborders/menu/?establishment={estab}"
    response = requests.request('GET', url, headers=headers)
    response_body = json.loads(response.text)
    categories = response_body['data']['categories']

    names = []
    prices = []

    for category in categories:
        products = category['products']
        for product in products:
            names.append(product['name'])
            prices.append(product['price'])

    return names, prices


def print_products(names, prices):
    i = 0
    for name in names:
        print(f"{name} - ${prices[i]}")
        i+=1

names, prices = get_menu()
print_products(names, prices)