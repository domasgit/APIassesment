from secrets import baseurl, estab, key, secret
import requests, json

headers		= {
	'Content-Type'			: 'application/json',
	'Accept'				: 'application/json',
	'API-AUTHENTICATION'	: key + ':' + secret
}

def get_menu():
    url = f"{baseurl}/weborders/menu/?establishment={estab}&mode=0"
    response = requests.request('GET', url, headers=headers)
    response_body = json.loads(response.text)
    categories = response_body['data']['categories']

    names = []
    prices = []
    prod_ids = []
    required_mods = []#used in task 3
    minimum_amounts = []#used in task 3

    for category in categories:
        products = category['products']

        for product in products:
            names.append(product['name'])
            prices.append(product['price'])
            prod_ids.append(product['id'])

            minimum_amount = 0
            modifiers = []

            for mod_class in product['modifier_classes']:
                if (mod_class['minimum_amount'] is not None and (minimum_amount == 0 or mod_class['minimum_amount'] < minimum_amount)):
                    minimum_amount = mod_class['minimum_amount']
                    modifiers = [
                        {"id": modifier['id'],  "name": modifier['name'], "price": modifier['price']}
                        for modifier in mod_class['modifiers']
                    ]
            minimum_amounts.append(minimum_amount)
            required_mods.append(modifiers)


    return names, prices, prod_ids, minimum_amounts, required_mods


def print_products(names, prices, prod_ids):
    for name, price, prod_id in zip(names, prices, prod_ids):
        print(f"[#{prod_id}]{name} - ${price}")

def main():
    names, prices, prod_ids, _, _ = get_menu()
    print_products(names, prices, prod_ids)

if __name__ == "__main__":
    main()