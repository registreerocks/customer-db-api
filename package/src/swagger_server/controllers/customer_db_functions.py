from bson import ObjectId
from pymongo import MongoClient, ReturnDocument

from .authentication import requires_auth, requires_scope
from .helpers import check_id

client = MongoClient('mongodb://mongodb:27017/')
db = client.customer_database
customer_details = db.customer_details
payment_details = db.payment_details
invoices = db.invoices

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
def post_payment(body):
    return str(payment_details.insert_one(body).inserted_id)

@requires_auth
@requires_scope('registree', 'recruiter')
@check_id
def get_payment(id):
    result = payment_details.find_one({'_id': ObjectId(id)})
    if result:
        result['_id'] = str(result['_id'])
        return result
    else:
        return {'ERROR': 'No matching data found.'}, 409

@requires_auth
@requires_scope('registree', 'recruiter')
def get_payment_by_customer(customer_id):
    result = payment_details.find_one({'customer_id': customer_id})
    if result:
        result['_id'] = str(result['_id'])
        return result
    else:
        return {'ERROR': 'No matching data found.'}, 409

@requires_auth
@requires_scope('registree')
@check_id
def put_payment(id, body):
    result = payment_details.find_one_and_update(
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
def get_invoice_by_query(query_id):
    result = invoices.find_one({'query_id': query_id})
    if result:
        result['_id'] = str(result['_id'])
        return result
    else:
        return {'ERROR': 'No matching data found.'}, 409

@requires_auth
@requires_scope('registree', 'recruiter')
def get_invoices_by_customer(customer_id):
    result = invoices.find({'customer_id': customer_id})
    if result:
        return _stringify_object_id(result)
    else:
        return {'ERROR': 'No matching data found.'}, 409

@requires_auth
@requires_scope('registree', 'recruiter')
def get_invoices_by_customer_paid(customer_id):
    result = invoices.find({'customer_id': customer_id, 'payment.complete': 'true'})
    if result:
        return _stringify_object_id(result)
    else:
        return {'ERROR': 'No matching data found.'}, 409
    
@requires_auth
@requires_scope('registree', 'recruiter')
def get_invoices_by_customer_open(customer_id):
    result = invoices.find({'customer_id': customer_id, 'payment.complete': 'false'})
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

def _stringify_object_id(result):
    stringified_result = []
    for element in result:
        element['_id'] = str(element['_id'])
        stringified_result.append(element)
    return stringified_result