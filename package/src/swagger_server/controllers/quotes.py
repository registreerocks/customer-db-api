import math
from os import environ as env

BASE_RATE = env.get('BASE_RATE', 2500)
TIER_RATES = [
  env.get('TIER_1_RATE', 200),
  env.get('TIER_2_RATE', 175),
  env.get('TIER_3_RATE', 150),
  env.get('TIER_4_RATE', 125),
  env.get('TIER_5_RATE', 100),
  env.get('TIER_6_RATE', 75)
]

TIERS = [
  0,
  env.get('TIER_1', 10),
  env.get('TIER_2', 50),
  env.get('TIER_3', 100),
  env.get('TIER_4', 150),
  env.get('TIER_5', 200)
]

def _quote_info(n):
  return {
    'numberOfStudents': n,
    'rsvpCostBreakdown': [{'percent': i, 'cost': _calculate_quote(math.floor((i/100) * n))} for i in [5, 10, 20, 50, 100]]
  }


def _calculate_quote(n):
  total = BASE_RATE
  for i, tier in enumerate(TIERS[1:]):
    if n < tier:
      total += (n - TIERS[i]) * TIER_RATES[i]
      break
    else:
      total += (tier - TIERS[i]) * TIER_RATES[i]
  if n > TIERS[5]:
    total += (n - TIERS[5]) * TIER_RATES[5]
  return total
