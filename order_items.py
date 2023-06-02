from secrets import baseurl, estab, key, secret
import requests, json

headers		= {
	'Content-Type'			: 'application/json',
	'Accept'				: 'application/json',
	'API-AUTHENTICATION'	: key + ':' + secret
}

def get_newest_order ():
    url = f"{baseurl}/resources/Order/"
    params = {
        'order_by'      : "-created_date",
        'limit'         : "1",
        'establishment' : estab
    }
    response 	= requests.request('GET', url, headers=headers, params=params)
    data		= json.loads(response.text)
    order_id    = data['objects'][0]['id']

    return order_id

def get_order_items (order_id):
    url = f"{baseurl}/resources/OrderItem/"
    params = {
        'order': order_id
    }
    response 	= requests.request('GET', url, headers=headers, params=params)
    data = json.loads(response.text)

    ids = []
    names = []
    quantities = []
    prices = []
    taxes = []

    for order_item in data['objects']:
        ids.append(str(order_item['id']))
        names.append(str(order_item['product_name_override']))
        quantities.append(str(order_item['quantity']))
        prices.append(str(order_item['price']))
        taxes.append(str(order_item['tax_amount']))

    return ids, names, quantities, prices, taxes

def print_results (ids, names, quantities, prices, taxes):
    for id, name, quantity, price, tax in zip(ids, names, quantities, prices, taxes):
        print(f"[ID#{id}] {name} * qty: {quantity} Price ${price} + tax ${tax}")


def main():
    order_id = get_newest_order()
    print(f"Order: {order_id}")
    ids, names, quantities, prices, taxes = get_order_items(order_id)
    print_results(ids, names, quantities, prices, taxes)


if __name__ == "__main__":
    main()
