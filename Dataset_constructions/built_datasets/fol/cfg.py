from nltk import CFG

standard = CFG.fromstring("""
                E -> Q UP | Q Q BP | Q Q Q TP | E LO E
                UP -> "#""(""_"")"
                BP -> "#""(""_"",""_"")"
                TP -> "#""(""_"",""_"",""_"")"
                Q -> "∀""_" | "∃""_"
                LO -> "∧" | "∨" | "→"
                """)

standard2 = CFG.fromstring("""
                E -> Q UP | Q Q BP | Q Q Q TP | E LO E
                UP -> "#""(""_"")"
                BP -> "#""(""_"",""_"")"
                TP -> "#""(""_"",""_"",""_"")"
                Q -> "∃""_" | "∀""_"
                LO -> "∧" | "∨" | "→"
                """)

nested = CFG.fromstring("""
                E -> Predicate_E | Quantified_E | Quantifier_Part Predicate_E | Quantifier_Part2 Predicate_E2
                Predicate_E -> "U" '(' '_' ')'
                Predicate_E2 -> "B"'(' '_' ',' '@' ')'
                Quantified_E -> Quantifier_Part Predicate_E | Quantifier_Part '(' Predicate_E LO E ')' | Quantifier_Part '(' Quantifier_Part2 Predicate_E2 LO E ')'
                Quantifier_Part -> '∀' '_' | '∃' '_'
                Quantifier_Part2 -> '∀' '@' | '∃' '@'
                LO -> '∧' | '∨' | '→'
                """)

UniNL = CFG.fromstring("""
              S -> Part1 "→" Part
              Part -> Part2 | Part0"))" | Part0"→" UP"))" | Part0 LO BP"))"
              Part0 -> Part1 LO BP
              Part1 -> "∀""_" "(" UP 
              Part2 -> UP ")"
              LO -> "→" | "∧" 
              UP -> "U""(""_"")" | "¬" "U""(""_"")"
              BP -> "B""(""_"",""@"")" | "¬" "B""(""_"",""@"")"
              """)

ExiNL = CFG.fromstring("""
              S -> Part1 "∧" Part
              Part -> Part2 | Part0"))" | Part0"∧" UP"))" | Part0 LO BP"))"
              Part0 -> Part1 LO BP
              Part1 -> "∃""_" "(" UP 
              Part2 -> UP ")"
              LO -> "→" | "∧" 
              UP -> "U""(""_"")" | "¬" "U""(""_"")"
              BP -> "B""(""_"",""@"")" | "¬" "B""(""_"",""@"")"
              """)

