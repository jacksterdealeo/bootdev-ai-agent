
file_path = "pkg/calculator.py"
with open(file_path, 'r') as file:
    filedata = file.read()

# Replace the target string
filedata = filedata.replace('            "+": 3,', '            "+": 1,')
filedata = filedata.replace('            "-": 1,', '            "-": 1,')
filedata = filedata.replace('            "*": 2,', '            "*": 2,')
filedata = filedata.replace('            "/": 2,', '            "/": 2,')

# Write the file out again
with open(file_path, 'w') as file:
    file.write(filedata)
