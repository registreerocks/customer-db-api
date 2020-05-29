from os import environ as env

import requests
from bson import ObjectId
from pymongo import MongoClient, ReturnDocument
from registree_auth import check_user_id, requires_auth, requires_scope

from .helpers import _stringify_object_id, check_id
from .invoice import _update_invoice
from .quotes import _bulk_price, _calculate_quote, _quote_info
from .user import _request_management_token, _update_user

CLIENT = MongoClient(
    'mongodb://mongodb:27017/', 
    username=env.get('MONGO_USERNAME'), 
    password=env.get('MONGO_PASSWORD')
    )
DB = CLIENT.database
customer_details = DB.customer_details
invoices = DB.invoices

@requires_auth
@requires_scope('registree')
def post_customer(body):
    return str(customer_details.insert_one(body).inserted_id)

@requires_auth
@requires_scope('registree', 'recruiter')
@check_id
def get_customer(id):
    result = customer_details.find_one({'_id': ObjectId(id)})
    if result:
        result['_id'] = str(result['_id'])
        return result
    else:
        return {'ERROR': 'No matching data found.'}, 409

@requires_auth
@requires_scope('registree', 'recruiter')
@check_id
def put_customer(id, body):
    update = {item.get('field'): item.get('value') for item in body}
    result = customer_details.find_one_and_update(
                {'_id': ObjectId(id)},
                {'$set': update},
                return_document=ReturnDocument.AFTER
            )
    if result:
        result['_id'] = str(result['_id'])
        return result
    else:
        return {'ERROR': 'No matching data found.'}, 409

@requires_auth
@requires_scope('registree')
def get_all_customers():
    result = customer_details.find({})
    if result:
        return _stringify_object_id(result)
    else:
        return {'ERROR': 'No matching data found.'}, 409

@requires_auth
@requires_scope('registree')
def post_invoice(body):
    price = _calculate_quote(body.get('rsvp'))
    body['price'] = {
        'amount': price,
        'currency': 'ZAR'
    }
    return str(invoices.insert_one(body).inserted_id)

@requires_auth
@requires_scope('registree', 'recruiter')
@check_id
def get_invoice(id):
    result = invoices.find_one({'_id': ObjectId(id)})
    if result:
        result['_id'] = str(result['_id'])
        return result
    else:
        return {'ERROR': 'No matching data found.'}, 409

@requires_auth
@requires_scope('registree', 'recruiter')
def get_invoice_detailed(**kwargs):
    result = invoices.find(kwargs)
    if result:
        return _stringify_object_id(result)
    else:
        return {'ERROR': 'No matching data found.'}, 409

@requires_auth
@requires_scope('registree')
@check_id
def put_invoice(id, body):
    update = _update_invoice(body)
    result = invoices.find_one_and_update(
                {'_id': ObjectId(id)},
                {'$set': update},
                return_document=ReturnDocument.AFTER
            )
    if result:
        result['_id'] = str(result['_id'])
        return result
    else:
        return {'ERROR': 'No matching data found.'}, 409

@requires_auth
@requires_scope('recruiter')
@check_id
def get_quote(n):
    return _quote_info(n)

@requires_auth
@requires_scope('registree')
@check_id
def get_price(n):
    return _calculate_quote(n)

@requires_auth
@requires_scope('registree')
@check_id
def bulk_get_price(body):
    return _bulk_price(body)

@requires_auth
@requires_scope('recruiter')
@check_user_id
def update_user(id, body):
    try:
        access_token = _request_management_token()
        try:
            return _update_user(id, body, access_token)
        except requests.exceptions.HTTPError as e:
            return {'ERROR': 'Unable to update user. Status code: '+ str(e.response.status_code)}, 400
    except requests.exceptions.HTTPError as e:
        return {'ERROR': 'Unable to fetch management access token. Status code: '+ str(e.response.status_code)}, 400
