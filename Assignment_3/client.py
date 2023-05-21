from rpc_client import *
import string

res = multiply(1, 2)
print("Multiplication res: ", end="")
print(res)

res = addition(1, 2)
print("Addition res: ", end="")
print(res)

res = foo(1729)
print("foo res : ", end="")
print(res)

res = bar(1729, "kolkata")
print("bar result : ", end="")
print(res)

res = voidFunc("kolkata")

res = univAdd(12, 23.4434)
print("univAdd res: ", end="")
print(res)

res = boolOp(True, False)
print("boolOp res: ", end="")
print(res)

res = noParam()
print("noParam res: ", end="")
print(res)

noParamReturn()

# res = division(12.56, 0)
# print("Division res = ", end="")
# print(res)
