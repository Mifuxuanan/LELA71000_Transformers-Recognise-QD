def find_matching(FOL, i):
    cnt = 1
    for j in range(i + 1, len(FOL)):
        if FOL[j] == '(':
            cnt += 1
        elif FOL[j] == ')':
            cnt -= 1
            if cnt == 0:
                return j
    return -1

def parse(FOL, start=0, end=None, depth=0):
    if end is None:
        end = len(FOL)

    spans, max_depth = [], depth
    idx = start

    while idx < end - 1:
        if FOL[idx] in ('∀', '∃') and FOL[idx + 1].isalpha():
            chain = []
            while idx < end - 1 and FOL[idx] in ('∀', '∃') and FOL[idx + 1].isalpha():
                chain.append(FOL[idx:idx + 2])
                idx += 2
            L = idx                            

            if L < end and FOL[L] == '(':
                R = find_matching(FOL, L)
            else:
                j = FOL.find('(', L, end)
                R = find_matching(FOL, j) if j != -1 else end - 1

            d = depth + 1
            max_depth = max(max_depth, d + len(chain) - 1)

            for q in chain:
                spans.append([q, d, [L, R]])

            rec_start = L + 1 if L < end and FOL[L] == '(' else L
            sub_max, sub_spans = parse(FOL, rec_start, R, d)
            spans.extend(sub_spans)
            max_depth = max(max_depth, sub_max)

            idx = R              
        idx += 1                

    return max_depth, spans

def result(df):
    QD_col, QS_col = [],[]
    for idx, row in df.iterrows():
        fol = row["FOL"]
        QD, QS = parse("".join(fol.split()))
        
        QD_col.append(QD)
        QS_col.append(QS)

    df['QS'] = QS_col
    df['QD'] = QD_col
    return df