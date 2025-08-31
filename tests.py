from functions.run_python import run_python_file

# Test 1
# (should print the calculator's usage instructions)
print(run_python_file("calculator", "main.py"))

# (should run the calculator... which gives a kinda nasty rendered result)
print(run_python_file("calculator", "main.py", ["3 + 5"]))

print(run_python_file("calculator", "tests.py"))

# (this should return an error)
print(run_python_file("calculator", "../main.py"))

# (this should return an error)
print(run_python_file("calculator", "nonexistent.py"))


'''
# Test 1
directory = "calculator"
file = "lorem.txt"
content = "wait, this isn't lorem ipsum"
print(f"Result for Directory: {directory}\nFile: {file}\nContent: {content}")
result = write_file(directory, file, content)
print(result)
print()

# Test 2
directory = "calculator"
file = "pkg/morelorem.txt"
content = "lorem ipsum dolor sit amet"
print(f"Result for Directory: {directory}\nFile: {file}\nContent: {content}")
result = write_file(directory, file, content)
print(result)
print()

# Test 3
directory = "calculator"
file = "/tmp/temp.txt"
content = "this should not be allowed"
print(f"Result for Directory: {directory}\nFile: {file}\nContent: {content}")
result = write_file(directory, file, content)
print(result)
print()
'''
