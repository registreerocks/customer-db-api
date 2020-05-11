import math
from os import environ as env

import requests
from bson import ObjectId
from pymongo import MongoClient, ReturnDocument
from registree_auth import check_user_id, requires_auth, requires_scope

from .helpers import _stringify_object_id, check_id
from .quotes import _calculate_quote
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
@requires_scope('registree')
@check_id
def put_customer(id, body):
    result = customer_details.find_one_and_update(
                {'_id': ObjectId(id)},
                {'$set':{body.get('field'): body.get('value')}},
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
    if body.get('field') == 'complete':
        update = {'complete': body.get('value') == 'True' or body.get('value') == 'true'}
    elif body.get('field') == 'rsvp':
        update = {
            'rsvp': int(body.get('value')),
            'price.amount': _calculate_quote(int(body.get('value')))
        }
    else:
        update = {body.get('field'): body.get('value')}
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
    return [
        {
            'string': 'Number of students to be contacted given search criteria',
            'value': n
        },
        {
            'string': 'Total cost of query if 5% of students RSVP to attend the event',
            'value': 'R {:,}'.format(_calculate_quote(math.floor(0.05 * n)))
        },
        {
            'string': 'Total cost of query if 10% of students RSVP to attend the event',
            'value': 'R {:,}'.format(_calculate_quote(math.floor(0.1 * n)))
        },
        {
            'string': 'Total cost of query if 20% of students RSVP to attend the event',
            'value': 'R {:,}'.format(_calculate_quote(math.floor(0.2 * n)))
        }
    ]

@requires_auth
@requires_scope('registree')
@check_id
def get_price(n):
    return _calculate_quote(n)



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
