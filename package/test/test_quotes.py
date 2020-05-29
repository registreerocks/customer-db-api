from src.swagger_server.controllers.quotes import (_bulk_price,
                                                   _calculate_quote,
                                                   _quote_info)


def test_calculate_quote():
  assert(_calculate_quote(8) == 4100)
  assert(_calculate_quote(15) == 5375)
  assert(_calculate_quote(70) == 14500)
  assert (_calculate_quote(201) == 30325)

def test_quote_info():
  expected_output = {
    'numberOfStudents': 70,
    'rsvpCostBreakdown': 
    [
      {'cost': 3100, 'percent': 5},
      {'cost': 3900, 'percent': 10},
      {'cost': 5200, 'percent': 20},
      {'cost': 8875, 'percent': 50},
      {'cost': 14500, 'percent': 100}
    ]
  }
  assert(_quote_info(70) == expected_output)

def test_bulk_price():
  body = [
    {
      'query_id': '123',
      'n': 11
    }, {
      'query_id': '567',
      'n': 66
    }, {
      'query_id': '890',
      'n': 111
    }
  ]
  expected_output = [
    {
      'query_id': '123',
      'price': 4675
    }, {
      'query_id': '567',
      'price': 13900
    }, {
      'query_id': '890',
      'price': 20375
    }
  ]
  assert(_bulk_price(body) == expected_output)