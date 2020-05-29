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
  body = {
    '123': 11,
    '567': 66,
    '890': 111
  }
  expected_output = {
    '123': 4675,
    '567': 13900,
    '890': 20375
  }
  assert(_bulk_price(body) == expected_output)