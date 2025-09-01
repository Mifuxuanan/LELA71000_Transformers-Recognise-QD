# Pattern1:
## 1-1. ∀x(P(x)→∀y(Q(y)→R(x,y)))
## 1-2: ∀x(P(x)→∃y(Q(y)∧R(x,y)))
## 1-3: ∃x(P(x)∧∃y(Q(y)∧R(x,y)))
## 1-4: ∃x(P(x)∧∀y(Q(y)→R(x,y)))

# Pattern2: Pattern1 [∧|∨|→] Pattern1
# Pattern3: Pattern1 [∧|∨|→] ( Pattern1 [∧|∨|→] Pattern1 )

import pandas as pd
from .nl_cfg import NL_type2
from .fol2nl_generation import *
from built_datasets.data_config import *
from built_datasets.data_utils import generation

def raw_type2(n_data):
    # LO = 0
    sample1 = generation(NL_type2, n_data=n_data, depth=4, min_skip=0, max_skip=3, min_len=0, max_len=11)
    # LO = 1
    sample2 = generation(NL_type2, n_data=n_data, depth=5, min_skip=4, max_skip=51, min_len=11, max_len=24)
    # LO = 2
    sample3 = generation(NL_type2, n_data=n_data, depth=6, min_skip=8, max_skip=627, min_len=36, max_len=48)
    # # LO = 3
    # sample4 = generation(NL_type2, n_data=n_data, depth=6, min_skip=631, max_skip=1000, min_len=49, max_len=99)
    combined = sample1 + sample2 + sample3 #+ sample4
    return combined

def replace_ph_type2(fol_ls, var_set, ent, bp, div):
    result = []
    for fol in fol_ls:
        s = " ".join(fol)
        used_vars = set()
        used_pres = set()
        s, used_vars = replace(s, "_", 3, var_set, used_vars, exclude=True)
        s, used_vars = replace(s, "@", 3, var_set, used_vars, exclude=True)
        s, used_pres = replace(s, "#", 1, ent, used_pres, exclude=True)
        s, _ = replace(s, "*", div, bp, set(), exclude=False)
        result.append(s)
    return result

def replace_ph_order2(fol_ls, ent, bp, div):
    result = []
    for fol in fol_ls:
        s = " ".join(fol)
        used_var1 = set()
        used_var2 = set()
        used_pres = set()
        s, used_vars = replace_order(s, "_", 3, ["x", "z", "m"], used_var1, exclude=True)
        s, _ = replace_order(s, "@", 3, ["y", "w", "n"], used_var2, exclude=True)
        s, used_pres = replace(s, "#", 1, ent, used_pres, exclude=True)
        s, _ = replace(s, "*", div, bp, set(), exclude=False)
        result.append(s)
    return result

def main2(n_data, FOL_var_set, FOL_ent, FOL_bp, FOL_div,
                 FOL2NW_ent, FOL2NW_bp, FOL2NW_div):
  raw_FOL = raw_type2(n_data)

  FOL = replace_ph_type2(raw_FOL, FOL_var_set, FOL_ent, FOL_bp, FOL_div)
  FOL2NW = replace_ph_order2(raw_FOL, FOL2NW_ent, FOL2NW_bp, FOL2NW_div)
  df = pd.DataFrame(FOL, columns=['FOL'])
  df["FOL2NW"] = FOL2NW
  return df.drop_duplicates()

def parse_quanti2(s):
  s = s.replace(" ", "")
  s = strip_parens(s)
  def parse_sub(s):
    q = s[0]
    fol = s[s.find("(") + 1 : -1]
    idx, LO = top_LO(fol)
    if q == "∀" and LO == "→":
        left, right = fol.split("→", 1)
        temp = "all {}"
        return right, temp.format(parse_pre(left))
    elif q == "∃" and LO == "∧":
        left, right = fol.split("∧", 1)
        temp = "some {}"
        return right, temp.format(parse_pre(left))
    return None

  right, temp_r = parse_sub(s)
  right = strip_parens(right)
  right_r, temp_rr = parse_sub(right)
  pre = parse_pre(right_r)
  return temp_r + " "+ pre + " " + temp_rr

NL_type2_FOL = main2(n_data, var_set, set1, set2, 1,
                 person, bin_pre, 1)
FOL2NS_type2 = main_fol2ns(NL_type2_FOL, parse_quanti2, 2)

if __name__ == "__main__":
    FOL2NS_type2.to_json("FOL2NS_type2.json", orient="records", lines=True, force_ascii=False)