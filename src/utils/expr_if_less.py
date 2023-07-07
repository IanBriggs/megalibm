class ExprIfLess:
    def __init__(self, true_expr = None, false_expr = None, return_type = "double", compute="double", out_cast=False) -> None:
        self.true_expr = true_expr
        self.false_expr = false_expr
        self.return_type = return_type
        self.compute_type = compute
        self.out_cast = out_cast