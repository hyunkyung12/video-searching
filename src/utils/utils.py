import re

def remove_parenthesis(s):
    s = re.sub('\([ 가-힣a-z0-9]*\)','',s)
    return s
