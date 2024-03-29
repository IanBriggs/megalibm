
import lego_blocks
import fpcore
from numeric_types import FPDD


class SplitDomain(lego_blocks.LegoBlock):

    def __init__(self, numeric_type, in_names, out_names, domains_to_lego, useDD):
        super().__init__(numeric_type, in_names, out_names)
        assert (len(self.in_names) == 1)
        assert (len(self.out_names) == 1)

        self.domains_to_lego = domains_to_lego
        self.useDD = useDD

    def __repr__(self):
        msg = "SplitDomain({}, {}, {}, {})"
        return msg.format(repr(self.numeric_type),
                          repr(self.in_names),
                          repr(self.out_names),
                          repr(self.domains_to_lego))

    def to_c(self):
        cdecl = self.numeric_type.c_type
        out_cdecl = cdecl
        if self.useDD:
            out_cdecl = FPDD.c_type
        source_lines = [
            f"{out_cdecl} {self.out_names[0]};",
        ]

        points = [(dom, lego) for dom, lego in self.domains_to_lego.items()
                  if dom.inf == dom.sup]
        points.sort(key=lambda tup: tup[0].inf)
        for tup in points:
            dom, lego = tup
            inf = self.numeric_type.num_to_str(dom.inf)
            source_lines.append(f"if ({self.in_names[0]} == {inf}) {{")
            source_lines.append(f"    {cdecl} {lego[0].in_names[0]} = {self.in_names[0]};")
            for le in lego:
                source_lines += ["    " + l for l in le.to_c()]
            source_lines.append(f"    {self.out_names[0]} = {lego[-1].out_names[0]};")
            source_lines.append("} else")

        non_points = [(dom, lego) for dom, lego in self.domains_to_lego.items()
                  if dom.inf != dom.sup]
        points.sort(key=lambda tup: tup[0].inf)
        for tup in non_points:
            dom, lego = tup
            inf = self.numeric_type.num_to_str(dom.inf)
            sup = self.numeric_type.num_to_str(dom.sup)
            source_lines.append(f"if ({inf} <= {self.in_names[0]} && {self.in_names[0]} <= {sup}) {{")
            source_lines.append(f"    {cdecl} {lego[0].in_names[0]} = {self.in_names[0]};")
            for le in lego:
                source_lines += ["    " + l for l in le.to_c()]
            source_lines.append(f"    {self.out_names[0]} = {lego[-1].out_names[0]};")
            source_lines.append("} else")

        for i in range(len(source_lines)-1, 0, -1):
            if source_lines[i].startswith("if"):
                source_lines[i] = "{"
                break
        source_lines[-1] = "}"

        return source_lines