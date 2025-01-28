
from logic_bank.logic_bank import Rule
from database.models import *

def init_rule():
  Rule.constraint(validate=User,
                  as_condition=lambda row: row.password != '',
                  error_msg='Password must be set and non-empty')
