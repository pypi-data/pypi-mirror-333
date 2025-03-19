import re
from typing import Generator
from typing import Any, Tuple, Dict, List
# from .exceptions import NestedParenthesesError, ParenthesesMismatchError, ClosedParenthesesBeforeOpenError
from .exceptions import ParenthesesMismatchError, ClosedParenthesesBeforeOpenError

RE_SIGNED_NUMBER:str = r"(^(?=.)([+-]?([0-9]*)(\.([0-9]+))?)([eE][+-]?\d+)?)"
RE_NUMBER:str        =      r"(^(?=.)(([0-9]*)(\.([0-9]+))?)([eE][+-]?\d+)?)"
RE_LETTERS:str = r"^[a-zA-Z-+]+"

# function to return index of all instances of a substring in a string
def find_all(sub:str, a_str:str) -> Generator[int , Any , None]:
    start:int = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

# functions to parse elemental formulas (handles both floats and ints)
def get_first_elem(formula:str) -> Tuple[str, bool]:
    needed_split:bool = False
    for char in formula:
        if formula.find(char) != 0 and (char.isupper() or char == "+" or char == "-"):
            formula = formula.split(char)[0]
            needed_split = True
            return formula, needed_split
        
        char_ind = list(find_all(char, formula))
        if len(char_ind) > 1 and (char.isupper() or char == "+" or char == "-") and (formula[1] == char or formula[1].islower()) and sum(1 for c in formula[0:char_ind[1]] if c.isupper())==1:
            formula = formula[0:char_ind[1]]
            needed_split = True
            return formula, needed_split

    return formula, needed_split

def inner_parse_formula(text:str) -> Dict[str, float]:
    formula_dict:Dict[str,float] = {}
    for _ in range(0, len(text)):
        element = re.findall(RE_LETTERS, text)
        if len(element) == 0:
            break
        else:
            element, needed_split = get_first_elem(element[0])
            text = text.replace(element, '', 1)
            if needed_split:
                number = 1.0
            else:
                try:
                    number = float(re.findall(RE_SIGNED_NUMBER, text)[0][0])
                except:
                    number = 1.0
                text = re.sub(RE_SIGNED_NUMBER, "", text)
            if element not in list(formula_dict.keys()):
                formula_dict[element] = number
            else:
                formula_dict[element] += number
    return formula_dict

def find_occurrences(s:str, ch:str) -> List[int]:
    return [i for i, letter in enumerate(s) if letter == ch]
def get_first_parenth_match(text:str) -> int:
    position:int = -1
    ch_number:int = 0
    closed_parenth_count: int = 0
    opened_parenth_count: int = 0
    for ch in text:
        if ch == '(':
            opened_parenth_count += 1
        elif ch == ')':
            closed_parenth_count += 1
            if opened_parenth_count == closed_parenth_count:
                position = closed_parenth_count - 1
                break
        ch_number += 1

    return position

def parse_formula(text:str) -> Dict[str, float]:
    
    text = str(text)
    text = text.replace("[", "(")
    text = text.replace("]", ")")
    
    # get indices of starting parentheses "(" and ending ")"
    open_parenth_idx_list = find_occurrences(text, "(")
    closed_parenth_idx_list = find_occurrences(text, ")")
    
    if len(open_parenth_idx_list) != len(closed_parenth_idx_list):
        raise ParenthesesMismatchError(text)
    
    for i in range(0, len(open_parenth_idx_list)-1):
        # if open_parenth_idx_list[i+1] < closed_parenth_idx_list[i]:
        #     raise NestedParenthesesError(text)
        if closed_parenth_idx_list[i] < open_parenth_idx_list[i]:
            raise ClosedParenthesesBeforeOpenError(text)
        if i == len(open_parenth_idx_list)-1:
            if closed_parenth_idx_list[i+1] < open_parenth_idx_list[i+1]:
                raise ClosedParenthesesBeforeOpenError(text)
    
    seg_dict_list:List[Dict[str,float]] = []
    parenth_pairs_count = len(open_parenth_idx_list)
    for _ in range(parenth_pairs_count):
        text = str(text)
        if len(text) <= 0:
            break
        if not '(' in text and not ')' in text:
            break
        
        # get indices of starting parentheses "(" and ending ")"
        open_parenth_idx_list = find_occurrences(text, "(")
        closed_parenth_idx_list = find_occurrences(text, ")")

        first_parenth_match:int = get_first_parenth_match(text)
        if first_parenth_match < 0:
            raise ParenthesesMismatchError(text)
        seg = text[open_parenth_idx_list[0]:closed_parenth_idx_list[first_parenth_match]+1]
        
        try:
            number = float(re.findall(RE_SIGNED_NUMBER, text[closed_parenth_idx_list[first_parenth_match]+1:])[0][0])
        except:
            number = 1
        
        seg_no_parenth = seg[1:-1]
        # nested_parenth:bool = False
        if '(' in seg_no_parenth or ')' in seg_no_parenth:
            seg_formula_dict = parse_formula(seg_no_parenth)
            # nested_parenth = True

        else:
            seg_formula_dict = inner_parse_formula(seg_no_parenth)
        seg_formula_dict_mult = {k:v*number for (k,v) in seg_formula_dict.items()}

        endseg = re.sub(RE_NUMBER, "", text[closed_parenth_idx_list[first_parenth_match]+1:])
        # if not nested_parenth:
        text = text[:open_parenth_idx_list[0]]+endseg
        seg_dict_list.append(seg_formula_dict_mult)

    if '(' in text in text:
        seg_dict_list.append(parse_formula(text))
    else:
        seg_dict_list.append(inner_parse_formula(text))

    # merge and sum all segments
    if len(seg_dict_list) > 1:
        start_dict = seg_dict_list[0]
        for i in range(1, len(seg_dict_list)):
            next_dict = seg_dict_list[i]
            start_dict = { k: start_dict.get(k, 0) + next_dict.get(k, 0) for k in set(start_dict) | set(next_dict) }
        return start_dict
    else:
        return seg_dict_list[0]
    