import random
import pandas as pd
from data_utils import top_LO, generation
from data_config import *
from .cfg import standard, standard2
from .extract_qd import result
random.seed(42)

n_data = 1500

def replace_ph_FOL(fol:str, var_set, pre_set, used_var=None, used_preds=None):
  if used_var is None: used_var = set()
  if used_preds is None: used_preds = set()
  
  idx, LO = top_LO(fol)
  if LO:
    left = replace_ph_FOL(fol[:idx], var_set, pre_set, used_var=used_var, used_preds=used_preds)
    right = replace_ph_FOL(fol[idx+1:], var_set, pre_set, used_var=used_var, used_preds=used_preds)
    return left + LO + right

  var_stack = []
  new_fol = []
  depth = 0
  arg_idx = None

  for idx, item in enumerate(fol):
    if item in ("∀","∃"):
      new_fol.append(item)
      if fol[idx+1] == "_":
        var = random.choice(list(var_set - used_var))
        used_var.add(var)
        var_stack.append((depth, var))
        continue
    elif item == "(":
      depth += 1
      if fol[idx-1].isupper() or fol[idx-1] == "#":
        arg_idx = 0
      new_fol.append(item)
      continue
    elif item == ")":
      depth -= 1
      arg_idx = None
      while var_stack and var_stack[-1][0] > depth:
        var_stack.pop()
      new_fol.append(item)
      continue

    elif item == "_":
      if arg_idx is None:
        new_fol.append(var_stack[-1][1])
      else:
        if arg_idx >= len(var_stack):
          raise ValueError("num_argment more than bound variables!")
        new_fol.append(var_stack[arg_idx][1])
        arg_idx += 1
      continue

    elif item == "#":
      avail = list(pre_set - used_preds)
      if not avail:
          raise ValueError("no available predicate left!")
      new = random.choice(avail)
      used_preds.add(new)
      new_fol.append(new)
    else:
      new_fol.append(item)

  return "".join(new_fol)

def type1(n_data):
    # QD = 1
    sample1 = generation(standard, n_data=round(n_data*4), depth=3, min_skip=0, max_skip=1, min_len=0, max_len=7)
    # QD = 2
    sample2 = generation(standard, n_data=n_data, depth=3, min_skip=2, max_skip=5, min_len=7, max_len=11)
    # QD = 3
    sample3 = generation(standard, n_data=n_data, depth=3, min_skip=6, max_skip=13, min_len=11, max_len=15)
    combined = sample1 + sample2 + sample3
    return combined

def type2(n_data):
    # QD = 1
    sample1 = generation(standard, n_data=n_data, depth=4, min_skip=14, max_skip=85, min_len=13, max_len=14)
    # QD = 2
    sample2 = generation(standard, n_data=round(n_data*1.45), depth=4, min_skip=16, max_skip=257, min_len=17, max_len=22)
    # QD = 3
    sample3 = generation(standard, n_data=round(n_data*0.56), depth=4, min_skip=20, max_skip=601, min_len=21, max_len=30)
    combined = sample1 + sample2 + sample3
    return combined

# Only the first 615 samples for both cfg
def type3(n_data):
    # Start with "∀"
    ## QD = 1S
    sample1_1 = generation(standard, n_data=n_data/2, depth=5, min_skip=28, max_skip=99, min_len=20, max_len=21)
    ## QD = 2
    sample1_2 = generation(standard, n_data=round((n_data/2)*1.76), depth=5, min_skip=30, max_skip=481, min_len=24, max_len=29)
    ## QD = 3
    sample1_3 = generation(standard, n_data=round((n_data/2)*0.25), depth=5, min_skip=34, max_skip=615, min_len=28, max_len=45)
    
    # Start with "∃"
    ## QD = 1
    sample2_1 = generation(standard2, n_data=n_data/2, depth=5, min_skip=28, max_skip=99, min_len=20, max_len=21)
    ## QD = 2
    sample2_2 = generation(standard2, n_data=round((n_data/2)*1.76), depth=5, min_skip=30, max_skip=481, min_len=24, max_len=29)
    ## QD = 3
    sample2_3 = generation(standard2, n_data=round((n_data/2)*0.25), depth=5, min_skip=34, max_skip=615, min_len=28, max_len=45)

    combined = sample1_1 + sample1_2 + sample1_3 + sample2_1 + sample2_2 + sample2_3
    return combined

def main_FOL(n_data, type_fn):
  FOL = []
  raw_FOL = type_fn(n_data)  
  for s in raw_FOL:
    s = "".join(s)
    fol = replace_ph_FOL(s, var_set, pre_set, used_var=None, used_preds=None)
    FOL.append(fol)

    df = pd.DataFrame(FOL, columns=['FOL']).sample(frac=1).reset_index(drop=True)
  return df.drop_duplicates()

type1_FOL = main_FOL(n_data, type1)
type1_with_QD = result(type1_FOL)

type2_FOL = main_FOL(n_data, type2)
type2_with_QD = result(type2_FOL)

type3_FOL = main_FOL(n_data, type3)
type3_with_QD = result(type3_FOL)