
from logic_bank.logic_bank import Rule
from database.models import *

def init_rule():
  Rule.constraint(validate=Comment,
      as_condition=lambda row: row.user_id is not None,
      error_msg='A comment must be associated with a user')
