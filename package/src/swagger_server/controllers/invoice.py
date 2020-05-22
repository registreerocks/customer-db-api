from .quotes import _calculate_quote

def _update_invoice(body):
  data = {}
  for item in body:
    if item.get('field') == 'complete':
      data['complete'] = item.get('value') == 'True' or item.get('value') == 'true'
    elif item.get('field') == 'rsvp':
        data['rsvp'] = int(item.get('value'))
        data['price.amount'] = _calculate_quote(int(body.get('value')))
    else:
      data[item.get('field')] = item.get('value')
  return data
