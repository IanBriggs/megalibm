
import lego_blocks
import fpcore


class SplitDomain(lego_blocks.LegoBlock):

    def __init__(self, numeric_type, in_names, out_names, domains_to_lego):
        super().__init__(numeric_type, in_names, out_names)
        assert (len(self.in_names) == 1)
        assert (len(self.out_names) == 1)

        self.domains_to_lego = domains_to_lego

    def __repr__(self):
        msg = "SplitDomain({}, {}, {}, {})"
        return msg.format(repr(self.numeric_type),
                          repr(self.in_names),
                          repr(self.out_names),
                          repr(self.domains_to_lego))

    def to_c(self):
        source_lines = [
            f"{self.numeric_type.c_type()} {self.out_names[0]};",
        ]

        points = [(dom, lego) for dom, lego in self.domains_to_lego.items()
                  if dom.inf == dom.sup]
        points.sort(key=lambda tup: tup[0].inf)
        for tup in points:
            dom, lego = tup
            source_lines.append(f"if ({self.in_names[0]} == {dom.inf}) {{")
            source_lines.append(f"    {self.numeric_type.c_type()} {lego[0].in_names[0]} = {self.in_names[0]};")
            for le in lego:
                source_lines += ["    " + l for l in le.to_c()]
            source_lines.append(f"    {self.out_names[0]} = {lego[-1].out_names[0]};")
            source_lines.append("} else")

        non_points = [(dom, lego) for dom, lego in self.domains_to_lego.items()
                  if dom.inf != dom.sup]
        points.sort(key=lambda tup: tup[0].inf)
        for tup in non_points:
            dom, lego = tup
            source_lines.append(f"if ({self.in_names[0]} <= {dom.sup}) {{")
            source_lines.append(f"    {self.numeric_type.c_type()} {lego[0].in_names[0]} = {self.in_names[0]};")
            for le in lego:
                source_lines += ["    " + l for l in le.to_c()]
            source_lines.append(f"    {self.out_names[0]} = {lego[-1].out_names[0]};")
            source_lines.append("} else")

        source_lines[-1] = "}"

        return source_lines