

import lego_blocks


class Form(lego_blocks.LegoBlock):

    def __init__(self, numeric_type, in_names, out_names, *args):
        super().__init__(numeric_type, in_names, out_names)
        assert (len(self.in_names) == 1 or len(self.in_names)==2)
        assert (len(self.out_names) == 1)
