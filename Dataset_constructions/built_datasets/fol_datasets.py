from data_config import *
from fol.types123 import type1_with_QD, type2_with_QD, type3_with_QD
from fol.type4 import type4_with_QD
from data_utils import count_QD

QD1_1, QD1_2, QD1_3 = count_QD(type1_with_QD)
QD2_1, QD2_2, QD2_3 = count_QD(type2_with_QD)
QD3_1, QD3_2, QD3_3 = count_QD(type3_with_QD)
QD4_1, QD4_2, QD4_3 = count_QD(type4_with_QD)

print(f'---type1_example---\nf"QD=1: {QD1_1}, QD=2: {QD1_2}, QD=3: {QD1_3}"\n{type1_with_QD.head()}\n')
print(f'---type2_example---\nf"QD=1: {QD2_1}, QD=2: {QD2_2}, QD=3: {QD2_3}"\n{type2_with_QD.head()}\n')
print(f'---type3_example---\nf"QD=1: {QD3_1}, QD=2: {QD3_2}, QD=3: {QD3_3}"\n{type3_with_QD.head()}\n')
print(f'---type4_example---\nf"QD=1: {QD4_1}, QD=2: {QD4_2}, QD=3: {QD4_3}"\n{type4_with_QD.head()}\n')

if __name__ == "__main__":
    type1_with_QD.to_json("Type1_M.json", orient="records", lines=True, force_ascii=False)
    type2_with_QD.to_json("Type2_M.json", orient="records", lines=True, force_ascii=False)
    type3_with_QD.to_json("Type3_M.json", orient="records", lines=True, force_ascii=False)
    type4_with_QD.to_json("Type4_M.json", orient="records", lines=True, force_ascii=False)