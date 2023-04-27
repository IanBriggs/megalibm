

import lego_blocks


class GenerateCast(lego_blocks.LegoBlock):

    def __init__(self, numeric_type, in_names, out_names, cast):
        super().__init__(numeric_type, in_names, out_names)
        assert (len(self.in_names) == 1)
        assert (len(self.out_names) == 1)
        self.cast = cast

    def __repr__(self):
        msg = "GenerateCast({}, {}, {}, {}, {}, {}, {})"
        return msg.format(repr(self.numeric_type),
                          repr(self.in_names),
                          repr(self.out_names),
                          repr(self.cast))
            

    def to_c(self):
    
        lines = [
            f"{self.cast} {self.out_names[0]} = ({self.cast})({self.in_names[0]});"
        ]

        return lines
