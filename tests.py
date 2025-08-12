
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
