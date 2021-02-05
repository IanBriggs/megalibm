

import lego_blocks




class Case(lego_blocks.LegoBlock):

    def __init__(self, numeric_type, in_names, out_names, mod, cases):
        super().__init__(numeric_type, in_names, out_names)
        assert(len(self.in_names) == 2)
        assert(len(self.out_names) == 1)
        assert(type(mod) == int)
        assert(type(cases) == dict)
        assert(all(type(k) == int for k in cases.keys()))
        assert(all(i==j for i,j in zip(sorted(cases.keys()), range(mod))))
        assert(all(type(v) == str for v in cases.values()))

        self.mod = mod
        self.cases = cases


    def __repr__(self):
        return "Case({}, {}, {}, {}, {}, {})".format(repr(self.numeric_type),
                                                     repr(self.in_names),
                                                     repr(self.out_names),
                                                     repr(self.mod),
                                                     repr(self.cases))


    def to_c(self):
        fmt = {
            "k": self.in_names[1],
            "mod": self.mod,
            "out": self.out_names[0],
            "type": self.numeric_type.c_type(),
        }

        lines = [
            "{type} {out};".format(**fmt),
            "switch ({k}%{mod}) {{".format(**fmt),
        ]

        for c in sorted(self.cases.keys()):
            val = self.cases[c]
            code_case = [
                "    case {}:".format(c),
                "        {} = {};".format(fmt["out"], val),
                "        break;",
            ]
            lines += code_case

        final_case = [
            "    default:",
            "        assert(0);",
            "        return NAN;",
            "}",
        ]
        lines += final_case

        return lines
