import random
import itertools
from nltk.parse.generate import generate
random.seed(42)

def strip_outer_parens(fol):
  if type(fol) is list:
    if fol[0] == ("(") and fol[-1] == (")"):
        return fol[1:-1]
  elif type(fol) is str:
    fol = fol.strip()
    if fol.startswith("(") and fol.endswith(")"):
        return fol[1:-1]
  return fol

def top_LO(s):
    depth = 0
    for idx, tok in enumerate(s):
        if tok == "(":
            depth += 1
        elif tok == ")":
            depth -= 1
        elif depth == 0 and tok in "∧∨→":
            return idx, tok
    return -1, None

def random_skip(grammar, depth, min_skip, max_skip):
    outputs = generate(grammar, depth=depth)
    skip = random.randint(min_skip, max_skip)
    try:
        sent = next(itertools.islice(outputs, skip, None))
        return sent
    except StopIteration:
        return random_skip(grammar, depth, min_skip, max_skip)

def generation(grammar, n_data, depth, min_skip, max_skip, min_len, max_len):
    result = []
    while len(result)< n_data:
        outputs = random_skip(grammar, depth, min_skip, max_skip)
        if len(outputs) >= min_len and len(outputs) < max_len:
            result.append(strip_outer_parens(outputs))
    return result

def count_QD(df):
  QD1 = (df["QD"]==1).sum()
  QD2 = (df["QD"]==2).sum()
  QD3 = (df["QD"]==3).sum()
  return QD1, QD2, QD3

def count_QD_NL(df):
  QD1 = ((df["FOL"].str.count("∀") + df["FOL"].str.count("∃")) == 1)
  QD2 = ((df["FOL"].str.count("∀") + df["FOL"].str.count("∃")) == 2)
  return QD1.sum(), QD2.sum()



