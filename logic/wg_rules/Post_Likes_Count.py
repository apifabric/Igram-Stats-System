
from logic_bank.logic_bank import Rule
from database.models import *

def init_rule():
  Rule.count(derive=Post.likes_count, as_count_of=Like)
