from secrets import baseurl, estab, key, secret
from menu_retrieve import get_menu
import requests, json

headers		= {
	'Content-Type'			: 'application/json',
	'Accept'				: 'application/json',
	'API-AUTHENTICATION'	: key + ':' + secret
}

def prepare_products(names, prod_ids, prices, minimum_amounts, required_mods):
    products = []
    modifier_items = []
    for name, prod_id, price, minimum_amount, required_mod in zip(names, prod_ids, prices,minimum_amounts, required_mods):
        if minimum_amount > 0:
            print(f"Product {name} ID {prod_id} has required modifiers. Options:")
            i = 1
            for mod in required_mod:
                print(f"{i}. {mod['name']} ${mod['price']}")
                i+=1
            choice = int(input("Which modifier should be added?(enter the number before mod name):")) - 1

            selected_mod = required_mod[choice]
            modifier_item = {
                "product_id": prod_id,
                "modifier_price": selected_mod['price'],
                "qty": minimum_amount,
                "modifier": selected_mod['id']
            }

            modifier_items.append(modifier_item)

            product = {
                "modifieritems": modifier_items,
                "price": price,
                "product": prod_id,
                "quantity": 1
            }
            products.append(product)

        else:
            product = {
                "price": price,
                "product": prod_id,
                "quantity": 1
            }
            products.append(product)

    return products

def calculate_cart(products):    
    url = f"{baseurl}/specialresources/cart/calculate"
    body_data = {
        "items": products,
        "establishmentId": estab
    }
    payload = json.dumps(body_data)
    response = requests.request("POST", url, headers=headers, data=payload)
    response_body = json.loads(response.text)
    final_total = response_body['data']['final_total']
    subtotal = response_body['data']['subtotal']
    tax = response_body['data']['tax']

    return final_total, subtotal, tax




def main():
    names, prices, prod_ids, minimum_amounts, required_mods = get_menu()
    products= prepare_products(names, prod_ids, prices, minimum_amounts, required_mods)
    final_total, subtotal, tax = calculate_cart(products)
    print(f"Subtotal: ${subtotal}")
    print(f"Tax: ${tax}")
    print(f"Final Total: ${final_total}")

if __name__ == "__main__":
    main()