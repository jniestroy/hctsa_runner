import os

def add_imports(directory):
    # Define the imports to check and add
    required_imports = {
        "np": "import numpy as np\n",
        "stats": "from scipy import stats\n"
    }
    
    # List of all python files in the specified directory
    files = [f for f in os.listdir(directory) if f.endswith('.py')]
    
    for file in files:
        filepath = os.path.join(directory, file)
        with open(filepath, 'r') as f:
            content = f.readlines()
        
        # Determine which imports are needed
        need_np = 'np' in ''.join(content) and 'import numpy as np' not in ''.join(content)
        need_stats = 'stats' in ''.join(content) and 'from scipy import stats' not in ''.join(content)
        
        # Prepare the import string
        import_string = ''
        if need_np:
            import_string += required_imports['np']
        if need_stats:
            import_string += required_imports['stats']
        
        # If imports are needed, rewrite the file
        if import_string:
            with open(filepath, 'w') as f:
                f.write(import_string + ''.join(content))
            print(f"Updated '{file}' with necessary imports.")

# Specify the directory containing the Python files
directory_path = 'Operations'
add_imports(directory_path)
