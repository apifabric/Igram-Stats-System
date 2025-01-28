
from logic_bank.logic_bank import Rule
from database.models import *

def init_rule():
  Rule.constraint(validate=Profile,
                  as_condition=lambda row: row.user_id is not None,
                  error_msg='Each profile must be linked to a user')
