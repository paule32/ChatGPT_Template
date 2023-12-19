import marshal

with open('test.py', 'rb') as file:
    source_code = file.read()
    bytecode = marshal.dumps(compile(source_code, 'dummy', 'exec'))

print(bytecode)
