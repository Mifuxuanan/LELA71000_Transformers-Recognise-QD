import numpy as np
import pandas as pd
import random
import re
from built_datasets.data_config import *
from built_datasets.data_utils import random_skip, count_QD_NL
from .cfg import UniNL, ExiNL
from .extract_qd import result
random.seed(42)

def replace_ph_NL(fol, pre_set, var_set):
  var_stack = []
  depth = 0
  used_preds = set()
  used_var = set()
  new_fol = []
  var1, var2 = 0, 0
  total_var1 = fol.count("_")
  total_var2 = fol.count("@")
  for idx, tok in enumerate(fol):
    if tok in ("∀","∃"):
      new_fol.append(tok)
      nxt = fol[idx+1] if idx+1 < len(fol) else None
      if nxt in ("_", "@"):
        v = random.choice(list(set(var_set) - used_var)) if (set(var_set)-used_var) else "x"
        used_var.add(v)
        var_stack.append((depth, v))
    elif tok == "(":
      depth += 1
      new_fol.append(tok)
      continue

    elif tok == ")":
      depth -= 1                       
      while var_stack and var_stack[-1][0] > depth:  
          var_stack.pop()
      new_fol.append(tok)
      continue
    elif tok == "_":
      var1 += 1
      diff2 = total_var2 - var2
      diff1 = total_var1 - var1 
      if diff1 == 0 or diff1 == 0 and diff2 == 2: 
        new_fol.append(var_stack[0][1])
      elif diff1 == 1 and diff2 == 1:
        new_fol.append(var_stack[0][1])
      else:
        new_fol.append(var_stack[-1][1]) 
        continue 
    elif tok == "@":
      var2 += 1
      diff2 = total_var2 - var2 
      if diff2 == 0:
        new_fol.append(var_stack[-1][1])
      else:
        new_fol.append(var_stack[-2][1])
      continue
      
    elif tok in ("U","B"):
      avail = [p for p in pre_set if p not in used_preds]
      if not avail:
          raise ValueError("no available predicate left!")
      p = random.choice(avail)
      used_preds.add(p)
      new_fol.append(p)
      
    else:
      new_fol.append(tok)

  return "".join(new_fol)

def replace_ph_NL_order(fol, pre_set, var_set):
  var_stack = []
  depth = 0
  used_preds = set()
  used_var = set()
  new_fol = []
  var1, var2 = 0, 0
  total_var1 = fol.count("_")
  total_var2 = fol.count("@")
  for idx, tok in enumerate(fol):
    if tok in ("∀","∃"):
      new_fol.append(tok)
      nxt = fol[idx+1] if idx+1 < len(fol) else None
      if nxt in ("_", "@"):
        v = list(set(var_set) - used_var)[0] if (set(var_set)-used_var) else "x"
        used_var.add(v)
        var_stack.append((depth, v))
    elif tok == "(":
      depth += 1
      new_fol.append(tok)
      continue

    elif tok == ")":
      depth -= 1                       
      while var_stack and var_stack[-1][0] > depth:  
          var_stack.pop()
      new_fol.append(tok)
      continue
    elif tok == "_":
      var1 += 1
      diff2 = total_var2 - var2
      diff1 = total_var1 - var1 
      if diff1 == 0 or diff1 == 0 and diff2 == 2: 
        new_fol.append(var_stack[0][1])
      elif diff1 == 1 and diff2 == 1:
        new_fol.append(var_stack[0][1])
      else:
        new_fol.append(var_stack[-1][1]) 
        continue 
    elif tok == "@":
      var2 += 1
      diff2 = total_var2 - var2 
      if diff2 == 0:
        new_fol.append(var_stack[-1][1])
      else:
        new_fol.append(var_stack[-2][1])
      continue
      
    elif tok in ("U","B"):
      avail = [p for p in pre_set if p not in used_preds]
      if not avail:
          raise ValueError("no available predicate left!")
      p = avail[0]
      used_preds.add(p)
      new_fol.append(p)
      
    else:
      new_fol.append(tok)

  return "".join(new_fol)

def generationNL(grammar, n_data, depth, min_skip, max_skip, min_len, max_len, pre_set, var_set, replace_fn):
    result = []
    for _ in range(n_data):
        outputs = random_skip(grammar, depth, min_skip, max_skip)
        outputs = replace_fn(outputs, pre_set, var_set)
        if len(outputs) >= min_len and len(outputs) < max_len:
          result.append(outputs)
    return result

def main_NL(replace_fn):
    # QD=1
    ## "∀"
    sample1 = generationNL(UniNL, n_data=540, depth=5, min_skip=0, max_skip=3,
                min_len=13, max_len=16, pre_set=pre_NL, var_set=var_set, replace_fn=replace_fn)
    ## "∃"
    sample2 = generationNL(ExiNL, n_data=540, depth=5, min_skip=0, max_skip=3,
                min_len=13, max_len=16, pre_set=pre_NL, var_set=var_set, replace_fn=replace_fn)
    
    # QD=2 
    ## "∀"
    sample3 = generationNL(UniNL, n_data=510, depth=6, min_skip=2, max_skip=115,
                min_len=24, max_len=99, pre_set=pre_NL, var_set=var_NL, replace_fn=replace_fn)
    ## "∃"
    sample4 = generationNL(ExiNL, n_data=510, depth=6, min_skip=2, max_skip=115,
                min_len=24, max_len=99, pre_set=pre_NL, var_set=var_NL, replace_fn=replace_fn)

    combined = np.concatenate((sample1, sample2, sample3, sample4))
    inputs = pd.DataFrame(combined, columns=['FOL']).drop_duplicates()

    p_paren = re.compile(r'\(\s*(\w+)\s*,\s*\1\s*\)')
    mask_paren = inputs['FOL'].apply(lambda s: bool(p_paren.search(s)))
    df_clean = inputs[~mask_paren]
    p_LO = re.compile(r'(\w+\([^)]*\))\s*[∧∨→]\s*\1')
    mask_LO = df_clean['FOL'].apply(lambda s: bool(p_LO.search(s)))
    df_clean = df_clean[~mask_LO]

    Defined_FOL = df_clean.sample(frac=1).reset_index(drop=True)

    return Defined_FOL

def main_NL2(replace_fn):
    # QD=1
    ## "∀"
    sample1 = generationNL(UniNL, n_data=50, depth=5, min_skip=0, max_skip=3,
                min_len=13, max_len=16, pre_set=pre_NL, var_set=var_NL, replace_fn=replace_fn)
    ## "∃"
    sample2 = generationNL(ExiNL, n_data=50, depth=5, min_skip=0, max_skip=3,
                min_len=13, max_len=16, pre_set=pre_NL, var_set=var_NL, replace_fn=replace_fn)
    
    # QD=2 
    ## "∀"
    sample3 = generationNL(UniNL, n_data=500, depth=6, min_skip=2, max_skip=115,
                min_len=24, max_len=99, pre_set=pre_NL, var_set=var_NL, replace_fn=replace_fn)
    ## "∃"
    sample4 = generationNL(ExiNL, n_data=500, depth=6, min_skip=2, max_skip=115,
                min_len=24, max_len=99, pre_set=pre_NL, var_set=var_NL, replace_fn=replace_fn)

    combined = np.concatenate((sample1, sample2, sample3, sample4))
    inputs = pd.DataFrame(combined, columns=['FOL']).drop_duplicates()

    p_paren = re.compile(r'\(\s*(\w+)\s*,\s*\1\s*\)')
    mask_paren = inputs['FOL'].apply(lambda s: bool(p_paren.search(s)))
    df_clean = inputs[~mask_paren]
    p_LO = re.compile(r'(\w+\([^)]*\))\s*[∧∨→]\s*\1')
    mask_LO = df_clean['FOL'].apply(lambda s: bool(p_LO.search(s)))
    df_clean = df_clean[~mask_LO]
    
    Defined_FOL = df_clean.sample(frac=1).reset_index(drop=True)

    return Defined_FOL

typeNL1_FOL = main_NL(replace_ph_NL)
QD1, QD2 = count_QD_NL(typeNL1_FOL)
print(f'typeNL1_FOL: "QD=1":{QD1}, "QD=2":{QD2}')
typeNL1_with_QD = result(typeNL1_FOL)

typeNL2_FOL = main_NL2(replace_ph_NL_order)
QD1, QD2 = count_QD_NL(typeNL2_FOL)
print(f'typeNL2_FOL: "QD=1":{QD1}, "QD=2":{QD2}')
typeNL2_with_QD = result(typeNL2_FOL)