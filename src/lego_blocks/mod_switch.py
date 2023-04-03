
import lego_blocks
import fpcore


class ModSwitch(lego_blocks.LegoBlock):

    def __init__(self, numeric_type, in_names, out_names, mod_to_lego):
        super().__init__(numeric_type, in_names, out_names)
        assert (len(self.in_names) == 2)
        assert (len(self.out_names) == 1)

        self.mod_to_lego = mod_to_lego

    def to_c(self):
        cdecl = self.numeric_type.c_type()

        r = self.in_names[0]
        k = self.in_names[1]
        switch_out = self.out_names[0]

        mod = len(self.mod_to_lego)

        source_lines = [
            f"{cdecl} {switch_out};",
            f"switch ({k} % {mod}) {{",
        ]

        for i in range(mod):
            source_lines.append(f"    case ({i}): {{")
            legos = self.mod_to_lego[i]
            legos[0].in_names[0] = r
            legos[-1].out_names[0] = switch_out
            for le in legos:
                source_lines += ["        " + l for l in le.to_c()]
            source_lines[-1] = "        " + source_lines[-1].lstrip(f"        {cdecl}")
            source_lines.append("        } break;")

        source_lines.append("}")

        return source_lines