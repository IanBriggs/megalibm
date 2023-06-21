class ExprIfLess:
    def __init__(self, true_expr = None, false_expr = None, return_type = "double", compute="double") -> None:
        self.true_expr = true_expr
        self.false_expr = false_expr
        self.return_type = return_type
        self.compute_type = compute