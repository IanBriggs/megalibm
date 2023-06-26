from interval import Interval
import lambdas
from time_function import time_function

def time_lambda(domain: Interval,
                lambda_expression,
                name: str="lambda",
                samples: int = 1 << 17,
                iters: int = 1000):
    lambda_expression.type_check()
    #TODO:Handle Passing function names from lambdas
    lambda_function_name = "lambda"
    precision = lambda_expression.numeric_type
    _, lines = lambdas.generate_c_code(lambda_expression,
                                       lambda_function_name)
    lambda_code = "\n".join(lines)

    avg_run_time = time_function(numeric_type=precision,
                                 c_function_name=lambda_function_name,
                                 c_code=lambda_code,
                                 domain=domain,
                                 samples=samples,
                                 iters=iters)
    
    return avg_run_time