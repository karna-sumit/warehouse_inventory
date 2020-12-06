import requests
import error_messages

BUY_URL = "http://0.0.0.0:8080/buy"
GET_URL = "http://0.0.0.0:8080/"


def test_buy_positive():
    payload = {'product': "1000",
               'quantity': 1}

    headers = {'content_type': 'application/json'}

    response = requests.request("POST", BUY_URL, headers=headers, json=payload)

    assert response.text == 'OK'


def test_buy_bad_req1():
    payload = {
               'quantity': 1}

    headers = {'content_type': 'application/json'}

    response = requests.request("POST", BUY_URL, headers=headers, json=payload)

    assert response.text == error_messages.ERR_BAD_REQUEST.format('product')


def test_buy_bad_req2():
    payload = {
               'product': '1000'}

    headers = {'content_type': 'application/json'}

    response = requests.request("POST", BUY_URL, headers=headers, json=payload)

    assert response.text == error_messages.ERR_BAD_REQUEST.format('quantity')


def test_buy_not_enough_inventory():
    payload = {
               'product': '1000',
               'quantity': 100000}

    headers = {'content_type': 'application/json'}

    response = requests.request("POST", BUY_URL, headers=headers, json=payload)

    assert response.text == error_messages.ERR_NOT_ENOUGH_INVENTORY


def test_buy_product_not_found():
    payload = {
              'product': 'Invalid',
              'quantity': 1}

    headers = {'content_type': 'application/json'}

    response = requests.request("POST", BUY_URL, headers=headers, json=payload)

    assert response.text == error_messages.ERR_PROD_NOT_FOUND


def test_buy_neg_quantity():
    payload = {
               'product': '1000',
               'quantity': -1}

    headers = {'content_type': 'application/json'}

    response = requests.request("POST", BUY_URL, headers=headers, json=payload)

    assert response.text == error_messages.ERR_BAD_REQUEST.format('quantity')


def test_buy_zero_quantity():
    payload = {
               'product': '1000',
               'quantity': 0}

    headers = {'content_type': 'application/json'}

    response = requests.request("POST", BUY_URL, headers=headers, json=payload)

    assert response.text == error_messages.ERR_BAD_REQUEST.format('quantity')


def test_buy_no_payload():

    headers = {'content_type': 'application/json'}

    response = requests.request("POST", BUY_URL, headers=headers)

    assert response.text == error_messages.ERR_BAD_REQUEST.format('product quantity')


def test_list_products():

    headers = {'Content-Type': 'application/json'}

    response = requests.request("GET", GET_URL, headers=headers)

    assert response.status_code == 200


test_list_products()
test_buy_positive()
test_buy_bad_req1()
test_buy_bad_req2()
test_buy_neg_quantity()
test_buy_zero_quantity
test_buy_not_enough_inventory()
test_buy_product_not_found()
test_buy_no_payload()
print("All Good")
