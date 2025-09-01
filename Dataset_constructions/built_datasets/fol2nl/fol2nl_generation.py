import random
import itertools
from nltk.parse.generate import generate
from built_datasets.data_utils import top_LO

def strip_parens(s):
    while s.startswith("(") and s.endswith(")"):
        depth = 0
        balanced = True
        for idx, tok in enumerate(s):
            if tok == "(":
                depth += 1
            elif tok == ")":
                depth -= 1
                if depth == 0 and idx < len(s) - 1:
                    balanced = False
                    break
        if balanced:
            s = s[1:-1]
        else:
            break
    return s

def replace(step, sym, div, full_set, used_set, exclude):
    total = step.count(sym)
    n_group = total // div
    for _ in range(n_group+1):
        if exclude:
            choices = list(set(full_set) - used_set)
        else:
            choices = list(full_set)
        if not choices:
            raise ValueError(f"No more values available to replace '{sym}'!")
        pick = random.choice(choices)
        if exclude:
            used_set.add(pick)
        step = step.replace(sym, pick, div)
    return step, used_set

def replace_order(step, sym, div, full_vars, used_set, exclude):
    total = step.count(sym)
    n_group = total // div
    for _ in range(n_group+1):
        if exclude:
            choices = [v for v in full_vars if v not in used_set]
        else:
            choices = full_vars
        if not choices:
            choices = "x"
        pick = choices[0]
        if exclude:
            used_set.add(pick)
        step = step.replace(sym, pick, div)
    return step, used_set

def parse_pre(term):
    neg = term.startswith("¬")
    pre = term[1:term.find("(")] if neg else term[:term.find("(")]
    pre = pre.lower()
    if neg:
        return f"not {pre}"
    return pre

def fol_to_ns(fol, fn_quanti):
    s = fol.replace(" ", "")
    s = strip_parens(s)
    idx, LO = top_LO(s)
    if LO:
        left = fol_to_ns(s[:idx], fn_quanti)
        right = fol_to_ns(s[idx+1:], fn_quanti)
        if LO == "∧":
            return f"{left}, and {right}"
        if LO == "∨":
            return f"{left}, or {right}"
        if LO == "→":
            return f"{left}, which implies that {right}"
    if s.startswith(("∀", "∃")) and "(" in s and s.endswith(")"):
        return fn_quanti(s)
    return fol

def main_fol2ns(df, fn_quanti, QD):
  result = []
  for fol in df["FOL2NW"]:
    fol2ns = fol_to_ns(fol, fn_quanti).capitalize() + "."
    result.append(fol2ns)
  df["FOL2NS"] = result
  df["QD"] = QD
  return df
  