# Pattern1:
## 1-1. ∀x(P(x)→Q(x))
## 1-2: ∃x(P(x)∧Q(x))

# Pattern2: Pattern1 [∧|∨|→] Pattern1
# Pattern3: Pattern1 [∧|∨|→] ( Pattern1 [∧|∨|→] Pattern1 )

import pandas as pd
from .nl_cfg import NL_type1
from .fol2nl_generation import *
from built_datasets.data_config import *
from built_datasets.data_utils import generation

def raw_type1(n_data):
    # LO = 0
    sample1 = generation(NL_type1, n_data=n_data, depth=3, min_skip=0, max_skip=1, min_len=0, max_len=2)
    # LO = 1
    sample2 = generation(NL_type1, n_data=n_data, depth=4, min_skip=2, max_skip=9, min_len=2, max_len=6)
    # LO = 2
    sample3 = generation(NL_type1, n_data=n_data, depth=5, min_skip=4, max_skip=577, min_len=6, max_len=10)
    # # LO = 3
    # sample4 = generation(NL_type1, n_data=n_data, depth=5, min_skip=88, max_skip=589, min_len=13, max_len=99)
    combined = sample1 + sample2 + sample3 #+ sample4
    return combined

def replace_ph_type1(fol_ls, var_set, ent, up, div):
    result = []
    for fol in fol_ls:
        s = " ".join(fol)
        used_vars = set()
        s, used_vars = replace(s, "_", 3, var_set, used_vars, exclude=True)
        s, _ = replace(s, "#", div, ent, set(), exclude=False)
        s, _ = replace(s, "*", 1, up, set(), exclude=False)
        result.append(s)
    return result

def replace_ph_order(fol_ls, var_set, ent, up, div):
    result = []
    for fol in fol_ls:
        s = " ".join(fol)
        used_vars = set()
        s, used_vars = replace_order(s, "_", 3, var_set, used_vars, exclude=True)
        s, _ = replace(s, "#", div, ent, set(), exclude=False)
        s, _ = replace(s, "*", 1, up, set(), exclude=False)
        result.append(s)
    return result

def main_type1(n_data, FOL_var_set, FOL_ent, FOL_up, FOL_div,
         FOL2NW_var_set, FOL2NW_ent, FOL2NW_up, FOL2NW_div):
  raw_FOL = raw_type1(n_data)
  FOL = replace_ph_type1(raw_FOL, FOL_var_set, FOL_ent, FOL_up, FOL_div)
  FOL2NW = replace_ph_order(raw_FOL, FOL2NW_var_set, FOL2NW_ent, FOL2NW_up, FOL2NW_div)
  df = pd.DataFrame(FOL, columns=['FOL'])
  df["FOL2NW"] = FOL2NW
  return df.drop_duplicates()

def parse_quanti(s):
    q = s[0]
    fol = s[s.find("(") + 1 : -1]
    if q == "∀":
        left, right = fol.split("→", 1)
        temp_ls = ["all {} are {}", "all {}, without exception, are {}", "it is all {} who are {}", "it is the case that all {} are {}"]
        temp = random.choice(temp_ls)
    else:
        left, right = fol.split("∧", 1)
        temp_ls = ["some {} are {}", "some {}, without exception, are {}", "it is some {} who are {}", "it is the case that some {} are {}"]
        temp = random.choice(temp_ls)
    return temp.format(parse_pre(left), parse_pre(right))


NL_type1_FOL = main_type1(n_data, var_set, set1, set2, 1,
              ["x", "y", "z", "u"], person, un_pre, 1)
FOL2NS_type1 = main_fol2ns(NL_type1_FOL, parse_quanti, 1)

# if __name__ == "__main__":
#     FOL2NS_type1.to_json("FOL2NS_type1.json", orient="records", lines=True, force_ascii=False)