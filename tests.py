from functions.write_file import write_file


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

#
"""
from functions.get_file_content import get_file_content


# Test 1
directory = "calculator"
file = "main.py"
print(f"Result for directory: {directory}, file: {file}:")
result = get_file_content(directory, file)
print(result)

# Test 2
directory = "calculator"
file = "pkg/calculator.py"
print(f"Result for directory: {directory}, file: {file}:")
result = get_file_content(directory, file)
print(result)

# Test 3
directory = "calculator"
file = "/bin/cat"
print(f"Result for directory: {directory}, file: {file}:")
result = get_file_content(directory, file)
print(result)

# Test 4
directory = "calculator"
file = "pkg/does_not_exist.py"
print(f"Result for directory: {directory}, file: {file}:")
result = get_file_content(directory, file)
print(result)
"""


#
"""
# Test lorem.txt
print("Results for lorem.txt")
result = get_file_content("./calculator/", "lorem.txt")
print(result)
"""
#
"""
from functions.get_files_info import get_files_info


# Test 1: Current directory
print("Result for current directory:")
result = get_files_info("calculator", ".")
print(result)

# Test 2: pkg directory
print("Result for 'pkg' directory:")
result = get_files_info("calculator", "pkg")
print(result)

# Test 3: Outside working directory (/bin)
print("Result for '/bin' directory:")
result = get_files_info("calculator", "/bin")
print("    " + result)  # Add indentation for error messages

# Test 4: Outside working directory (../)
print("Result for '../' directory:")
result = get_files_info("calculator", "../")
print("    " + result)  # Add indentation for error messages
"""
