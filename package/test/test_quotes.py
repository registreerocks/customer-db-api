from src.swagger_server.controllers.quotes import _calculate_quote

def test_calculate_quote():
  assert(_calculate_quote(8) == 4100)
  assert(_calculate_quote(15) == 5375)
  assert(_calculate_quote(70) == 14500)
  assert (_calculate_quote(201) == 30325)