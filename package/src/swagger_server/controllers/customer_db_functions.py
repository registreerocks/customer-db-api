import math
from os import environ as env

from bson import ObjectId
from pymongo import MongoClient, ReturnDocument
from registree_auth import requires_auth, requires_scope

from .helpers import _stringify_object_id, check_id
from .quotes import _calculate_quote

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
    result = invoices.find_one_and_update(
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
@requires_scope('recruiter')
@check_id
def get_quote(n):
    return [
        {
            'string': 'Number of students to be contacted given search criteria',
            'value': n
        },
        {
            'string': 'Total cost of query given a 5% RSVP rate',
            'value': 'R {:,}'.format(_calculate_quote(math.floor(0.05 * n)))
        },
        {
            'string': 'Total cost of query given a 10% RSVP rate',
            'value': 'R {:,}'.format(_calculate_quote(math.floor(0.1 * n)))
        },
        {
            'string': 'Total cost of query given a 20% RSVP rate',
            'value': 'R {:,}'.format(_calculate_quote(math.floor(0.2 * n)))
        }
    ]

@requires_auth
@requires_scope('registree')
@check_id
def get_price(n):
    return _calculate_quote(n)
