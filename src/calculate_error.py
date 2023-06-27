import os
import os.path as path
import sys
import lambdas
# import interval

from numeric_types import NumericType

BIN_DIR = path.abspath(path.dirname(__file__))
GIT_DIR = path.split(BIN_DIR)[0]
EX_DIR = path.join(GIT_DIR, "examples")

# print(GIT_DIR)

# print(EX_DIR)

sys.path.append(EX_DIR)

# print(type(lambda_expression))



# sdfsf = "xyz"

if __name__ == "__main__":
    dsl_func_name = "dsl_amd_fast_asin"
    with open(EX_DIR + "/example.py", "r") as f:
        example = f.read()

    # print(example)
    example_globals = dict()
    exec(example, example_globals)
    lambda_expression = example_globals.get("lambda_expression")
    lambda_function_name = example_globals.get("lambda_function_name")
    
    lambda_expression.type_check()
    lambda_signature, lines = lambdas.generate_c_code(lambda_expression,
                                                      lambda_function_name)
    lambda_code = "\n".join(lines)

    print(lambda_code)

    print( example_globals.get("reference_impl"))

    print(lambda_function_name, )
