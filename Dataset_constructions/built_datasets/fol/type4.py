import numpy as np
import pandas as pd
import random
import re
from data_config import *
from data_utils import random_skip
from .cfg import nested
from .extract_qd import result
random.seed(42)

def replace_ph_type4(fol, pre_set, var_set):
  var1_stack = []
  var2_stack = []
  depth = 0
  used_U_preds, used_B_preds = set(), set()
  used_var = set()
  new_fol = []

  for idx, item in enumerate(fol):
    if item in ("∀","∃"):
      quanti = item
      if fol[idx+1] == "_":
        var1 = random.choice(list(var_set - used_var))
        used_var.add(var1)
        var1_stack.append([depth,var1])
        new_fol.append(quanti)
        continue
      elif fol[idx+1] == "@":
        var2 = random.choice(list(var_set - used_var))
        used_var.add(var2)
        var2_stack.append([depth,var2])
        new_fol.append(quanti)
        continue
    elif item == "(":
      new_fol.append(item)
      depth += 1
      continue
    elif item == ")":
      depth -= 1
      while var1_stack and var1_stack[-1][0] >= depth:
        var1_stack.pop()
      while var2_stack and var2_stack[-1][0] >= depth:
        var2_stack.pop()
      new_fol.append(item)
      continue
    elif item == "_":
      new_fol.append(var1_stack[-1][1])
      continue
    elif item == "@":
      new_fol.append(var2_stack[-1][1])
      continue
    elif item == "U":
      avail = [p for p in pre_set if p not in used_B_preds]
      if not avail:
          raise ValueError("no available unary predicate left!")
      new_U = random.choice(avail)
      used_U_preds.add(new_U)
      new_fol.append(new_U)
    elif item == "B":
      avail = [p for p in pre_set if p not in used_U_preds]
      if not avail:
          raise ValueError("no available binary predicate left!")
      new_B = random.choice(avail)
      used_B_preds.add(new_B)
      new_fol.append(new_B)
    else:
      new_fol.append(item)

  return "".join(new_fol)

def generation4(grammar, n_data, depth, min_skip, max_skip, min_len, max_len, pre_set, var_set):
    result = []
    for _ in range(n_data):
        outputs = random_skip(grammar, depth, min_skip, max_skip)
        outputs = replace_ph_type4(outputs, pre_set, var_set)
        if len(outputs) >= min_len and len(outputs) < max_len:
            result.append(outputs)
    return result

def main_type4():
    # QD=1
    sample1 = generation4(nested, n_data=7000, depth=5, min_skip=3, max_skip=28,
                min_len=13, max_len=14, pre_set=pre_set, var_set=var_set)
    # QD=2
    sample2 = generation4(nested, n_data=1600, depth=6, min_skip=4, max_skip=128,
                min_len=15, max_len=22, pre_set=pre_set, var_set=var_set)

    # QD=3
    sample3 = generation4(nested, n_data=1750, depth=7, min_skip=7, max_skip=580,
                min_len=24, max_len=31, pre_set=pre_set, var_set=var_set)

    combined = np.concatenate((sample1, sample2, sample3))
    inputs = pd.DataFrame(combined, columns=['FOL']).drop_duplicates()

    p_paren = re.compile(r'\(\s*(\w+)\s*,\s*\1\s*\)')
    mask_paren = inputs['FOL'].apply(lambda s: bool(p_paren.search(s)))
    df_clean = inputs[~mask_paren]
    p_LO = re.compile(r'(\w+\([^)]*\))\s*[∧∨→]\s*\1')
    mask_LO = df_clean['FOL'].apply(lambda s: bool(p_LO.search(s)))
    df_clean = df_clean[~mask_LO]

    Defined_FOL = df_clean.sample(frac=1).reset_index(drop=True)
    return Defined_FOL

type4_FOL = main_type4()
type4_with_QD = result(type4_FOL)