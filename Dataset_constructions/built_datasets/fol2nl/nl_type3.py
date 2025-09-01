# Pattern1:
## 1-1. ∀x(P(x)→∀y(Q(y)→∀z(S(z)→R(x,y,z))))
## 1-2. ∀x(P(x)→∃y(Q(y)∧∀z(S(z)→R(x,y,z))))
## 1-3. ∀x(P(x)→∀y(Q(y)→∃z(S(z)∧R(x,y,z))))
## 1-4. ∀x(P(x)→∃y(Q(y)∧∃z(S(z)∧R(x,y,z))))
## 1-5. ∃x(P(x)∧∃y(Q(y)∧∃z(S(z)∧R(x,y,z))))
## 1-6. ∃x(P(x)∧∀y(Q(y)→∃z(S(z)∧R(x,y,z))))
## 1-7. ∃x(P(x)∧∃y(Q(y)∧∀z(S(z)→R(x,y,z))))
## 1-8. ∃x(P(x)∧∀y(Q(y)→∀z(S(z)→R(x,y,z))))

# Pattern2: Pattern1 [∧|∨|→] Pattern1
# Pattern3: Pattern1 [∧|∨|→] ( Pattern1 [∧|∨|→] Pattern1 )

import pandas as pd
import random
from .nl_cfg import NL_type3, NL_type3_2
from .fol2nl_generation import *
from built_datasets.data_utils import strip_outer_parens, top_LO, generation
from built_datasets.data_config import *

def raw_type3(n_data):
    # LO = 0
    sample1 = generation(NL_type3, n_data=n_data, depth=3, min_skip=0, max_skip=7, min_len=0, max_len=2)
    # LO = 1
    sample2 = generation(NL_type3, n_data=n_data, depth=4, min_skip=7, max_skip=199, min_len=2, max_len=6)

    # LO = 2
    ## startwith "∀"
    sample3 = generation(NL_type3, n_data=n_data/2, depth=5, min_skip=15, max_skip=1000, min_len=6, max_len=10)
    ## startwith "∃"
    sample4 = generation(NL_type3_2, n_data=n_data/2, depth=5, min_skip=15, max_skip=1000, min_len=6, max_len=10)

    combined = sample1 + sample2 + sample3 + sample4
    return combined

def replace_ph_type3(fol:str, var_set, pre_set, used_var=None, used_preds=None):
  if used_var is None: used_var = set()
  if used_preds is None: used_preds = set()

  fol = strip_parens(fol)
  idx, LO = top_LO(fol)
  if LO:
    left = replace_ph_type3(fol[:idx], var_set, pre_set, used_var=used_var, used_preds=used_preds)
    right = replace_ph_type3(fol[idx+1:], var_set, pre_set, used_var=used_var, used_preds=used_preds)
    return "("+ left + LO + right + ")"

  var_stack = []
  new_fol = []
  depth = 0
  total_var = 0

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
      new_fol.append(item)
      continue
    elif item == ")":
      depth -= 1
      while var_stack and var_stack[-1][0] > depth:
        var_stack.pop()
      new_fol.append(item)
      continue

    elif item == "_":
      total_var += 1
      if total_var == 7:
        new_fol.append(var_stack[-3][1])
      elif total_var == 8:
        new_fol.append(var_stack[-2][1])
      else:
        new_fol.append(var_stack[-1][1])
      continue

    elif item in ("#", "@", "*"):
      avail = list(pre_set - used_preds)
      if not avail:
          raise ValueError("no available predicate left!")
      new = random.choice(avail)
      used_preds.add(new)
      new_fol.append(new)

    else:
      new_fol.append(item)

  return "".join(new_fol)

def replace_ph_type3_NW(fol, var_set, ent_set, item_set, tp_set,
                order=True, used_var=None, used_item=None, used_tp=None):
  if used_var is None: used_var = set()
#   if used_item is None: used_item = []
#   if used_tp is None: used_tp = []

  fol = strip_parens(fol)
  idx, LO = top_LO(fol)
  if LO:
    left = replace_ph_type3_NW(fol[:idx], var_set, ent_set, item_set, tp_set,
                  used_var=used_var, used_item=used_item, used_tp=used_tp)
    right = replace_ph_type3_NW(fol[idx+1:], var_set, ent_set, item_set, tp_set,
                  used_var=used_var, used_item=used_item, used_tp=used_tp)
    return f"({left}{LO}{right})"

  var_stack = []
  new_fol = []
  depth = 0
  total_var = 0

  for idx, item in enumerate(fol):
    if item in ("∀","∃"):
      new_fol.append(item)
      if fol[idx+1] == "_":
        pick = [v for v in var_set if v not in used_var]
        if order:
          var = var_set[len(used_var)]
        else:
          var = random.choice(pick)
        used_var.add(var)
        var_stack.append((depth, var))
        continue

    elif item == "(":
      depth += 1
      new_fol.append(item)
      continue
    elif item == ")":
      depth -= 1
      while var_stack and var_stack[-1][0] > depth:
        var_stack.pop()
      new_fol.append(item)
      continue

    elif item == "_":
      total_var += 1
      if total_var == 7:
        new_fol.append(var_stack[-3][1])
      elif total_var == 8:
        new_fol.append(var_stack[-2][1])
      else:
        new_fol.append(var_stack[-1][1])
      continue

    elif item == "#":
      new = random.choice(list(ent_set))
      new_fol.append(new)
      continue
    elif item == "@":
#       if used_item:
#         thing = used_item[0]
#       else:
      thing = random.choice(list(item_set))
#       used_item.append(thing)
      new_fol.append(thing)
      continue

    elif item == "*":
#       if used_tp:
#         tp = used_tp[0]
#       else:
      tp = random.choice(list(tp_set))
#         used_tp.append(tp)
      new_fol.append(tp)
      continue

    else:
      new_fol.append(item)

  return "".join(new_fol)

def main3(n_data, FOL_var, FOL_pre,
          FOL2NW_var, FOL2NW_ent, FOL2NW_item, FOL2NW_tp, order=True):
  raw_FOL = raw_type3(n_data)

  FOL, FOL2NW = [], []
  for s in raw_FOL:
    s = "".join(s)
    fol = replace_ph_type3(s, FOL_var, FOL_pre)
    fol2nw = replace_ph_type3_NW(s, FOL2NW_var, FOL2NW_ent, FOL2NW_item, FOL2NW_tp, order=True)
    FOL.append(strip_outer_parens(fol))
    FOL2NW.append(strip_outer_parens(fol2nw))

  df = pd.DataFrame(FOL, columns=['FOL'])
  df["FOL2NW"] = FOL2NW
  return df.drop_duplicates()

def parse_quanti3(s):
  s = strip_parens(s.replace(" ", ""))
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
    # else:
    #   raise ValueError(f"Unsupported pattern!")
    return None

  parts = []
  rest = s

  while True:
    rest_part = parse_sub(rest)
    if rest_part is None:
      break
    rest, ok = rest_part
    rest = strip_parens(rest)
    parts.append(ok)

  pre = parse_pre(rest)
  return f"{parts[0]} {pre} {parts[-1]} to {parts[1]}"

NL_type3_FOL = main3(n_data, var_set, pre_set,
          ["x", "y", "z", "u", "v", "w", "p", "q", "r"],
          person, thing, tern_pre, order=True)

FOL2NS_type3 = main_fol2ns(NL_type3_FOL, parse_quanti3, 3)

if __name__ == "__main__":
    FOL2NS_type3.to_json("FOL2NS_type3.json", orient="records", lines=True, force_ascii=False)