import logging
from logic_bank.logic_bank import DeclareRule, Rule, LogicBank
from database.models import *
from decimal import Decimal
from datetime import date, datetime

log = logging.getLogger(__name__)

def declare_logic():
    """
        declare_logic - declare rules
        this function is called from logic/declare_logic.py
    """
    log.info("declare_logic - active rules")
    
    # Exported Rules:
    # User Password Constraint 
    # Ensure the user password is set and not empty.
    Rule.constraint(validate=User,
                    as_condition=lambda row: row.password != '',
                    error_msg='Password must be set and non-empty')
    
    # Profile-User Link Constraint 
    # Ensure there is a user associated with each profile entry.
    Rule.constraint(validate=Profile,
                    as_condition=lambda row: row.user_id is not None,
                    error_msg='Each profile must be linked to a user')
    
    # Comment User Constraint 
    # Ensure each comment must be associated with a user.
    Rule.constraint(validate=Comment,
        as_condition=lambda row: row.user_id is not None,
        error_msg='A comment must be associated with a user')
    