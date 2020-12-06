import json
import logging
import os
from flask import Flask, request, make_response
import http
import error_messages

app = Flask(__name__)

# Common String literals

PRODUCT = 'product'
QUANTITY = 'quantity'
INVENTORY = 'inventory'
STOCK = 'stock'
AMOUNT_OF = 'amount_of'
ART_ID = 'art_id'
ID = 'id'
CONTAIN_ARTICLES = 'contain_articles'
CONTENT_TYPE = {'content_type': 'application/json'}


# Returns the products and the available stock

@app.route('/', methods=['GET'])
def get_all_products():
    try:
        available_products = []
        for product in get_products():
            stock = get_availabilty(product)
            available_products.append({PRODUCT: product, STOCK: stock})
        return make_response(json.dumps(available_products), http.HTTPStatus.OK, CONTENT_TYPE)
    except Exception as e:
        logging.error(e)
        return make_response(error_messages.ERR_GENERAL,
                             http.HTTPStatus.INTERNAL_SERVER_ERROR, CONTENT_TYPE)


# Checks availability and updates inventory

@app.route('/buy', methods=['POST'])
def buy_product():
    try:
        json = request.get_json()
        if json is None:
            return make_response(error_messages.ERR_BAD_REQUEST.format
                                 (PRODUCT + ' ' + QUANTITY), http.HTTPStatus.BAD_REQUEST, CONTENT_TYPE)
        product_id = json.get('product', None)
        quantity = json.get('quantity', 0)
        if product_id is not None and product_id != '':
            if isinstance(quantity, int) and quantity > 0:
                product = get_product(product_id)
                if product is not None:
                    if not get_availabilty(product) < quantity:
                        try:
                            update_inventory(product, quantity)
                        except Exception as e:
                            logging.error(e)
                            error_msg = error_messages.ERR_GENERAL
                            return make_response(error_msg,
                                                 http.HTTPStatus.INTERNAL_SERVER_ERROR, CONTENT_TYPE)
                        return make_response('OK', http.HTTPStatus.OK, CONTENT_TYPE)
                    else:
                        error_msg = error_messages.ERR_NOT_ENOUGH_INVENTORY
                        logging.error(error_msg)
                        return make_response(error_msg,
                                             http.HTTPStatus.INTERNAL_SERVER_ERROR, CONTENT_TYPE)
                else:
                    error_msg = error_messages.ERR_PROD_NOT_FOUND
                    logging.error(error_msg)
                    return make_response(error_msg,
                                         http.HTTPStatus.INTERNAL_SERVER_ERROR, CONTENT_TYPE)
            else:
                error_msg = error_messages.ERR_BAD_REQUEST.format(QUANTITY)
                logging.error(error_msg)
                return make_response(error_msg, http.HTTPStatus.BAD_REQUEST, CONTENT_TYPE)
        else:
            error_msg = error_messages.ERR_BAD_REQUEST.format(PRODUCT)
            logging.error(error_msg)
            return make_response(error_msg, http.HTTPStatus.BAD_REQUEST, CONTENT_TYPE)
    except Exception as e:
        logging.error(e)
        return make_response(error_messages.ERR_GENERAL,
                             http.HTTPStatus.INTERNAL_SERVER_ERROR, CONTENT_TYPE)


# Returns a particular product

def get_product(product_id):
    for product in get_products():
        if product[ID] == product_id:
            return product


# Returns the stock availability
# Assuming the least available article
# quanity is the least available
# product quantity

def get_availabilty(product):
    try:
        inventory_list = get_inventory()
        article_availability = []
        if product is not None:
            for article in product[CONTAIN_ARTICLES]:
                if (aa_id := article.get(ART_ID, None)) is not None:
                    for item in inventory_list:
                        print(type(item))
                        print(type(article))
                        item_id = item.get(ART_ID, None)
                        if aa_id == item_id:
                            try:
                                avail_qty = item.get(STOCK) / article.get(AMOUNT_OF)
                                article_availability.append(int(avail_qty))
                            except ZeroDivisionError:
                                logging.error(error_messages.ERR_INVALID_CONFIG.format(product[ID], aa_id))
                                return 0

        return min(article_availability) if len(article_availability) > 0 else 0
    except Exception as e:
        raise e


# Loads inventory

def get_inventory():
    try:
        with open('localdata/inventory.json', 'r') as inventory_file:
            inventory = json.load(inventory_file)[INVENTORY]
            inventory_file.close()
            return inventory
    except Exception as e:
        logging.error(e)
        raise e


# Loads products

def get_products():
    try:
        with open('localdata/products.json', 'r') as products_file:
            products = json.load(products_file)['products']
            products_file.close()
            return products
    except Exception as e:
        logging.error(e)
        raise e


# Updates inventory

def update_inventory(product, quantity):
    try:
        inventory_list = get_inventory()
        for article in product[CONTAIN_ARTICLES]:
            if (aa_id := article.get(ART_ID, None)) is not None:
                for item in inventory_list:
                    item_id = item.get(ART_ID, None)
                    if item_id == aa_id:
                        item[STOCK] = int(item[STOCK]) - quantity * int(article.get(AMOUNT_OF, 0))
            with open('localdata/inventory.json', 'w') as inventory:
                json.dump({INVENTORY: inventory_list}, inventory)
    except Exception as e:
        raise e


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
