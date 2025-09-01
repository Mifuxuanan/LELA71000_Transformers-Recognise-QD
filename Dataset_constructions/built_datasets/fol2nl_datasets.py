import pandas as pd
from built_datasets.fol2nl.nl_type1 import FOL2NS_type1
from built_datasets.fol2nl.nl_type2 import FOL2NS_type2
from built_datasets.fol2nl.nl_type3 import FOL2NS_type3

def main_dataset():
  return pd.concat([FOL2NS_type1, FOL2NS_type2, FOL2NS_type3], axis=0).sample(frac=1).reset_index(drop=True)

FOL2NS = main_dataset()
print(f'---FOL2NS_example---\n{FOL2NS.head()}\n')

if __name__ == "__main__":
    FOL2NS.to_json("FOL2NS.json", orient="records", lines=True, force_ascii=False)