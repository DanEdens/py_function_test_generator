import fnmatch
import os
import re


def find_def_or_class(root_dir):
    # Create an empty list to store the matching lines
    matching_lines = []

    # Create an empty list to store the file names
    python_files = []

    # Walk through the directories and files in the root directory
    for root, dirs, files in os.walk(root_dir):
        # Use fnmatch to filter the file names by the .py extension
        for name in fnmatch.filter(files, '*.py'):
            # Add the full file path to the list
            python_files.append(os.path.join(root, name))

    # Iterate through the Python files
    for file_name in python_files:
        # Open the file and read the lines
        with open(file_name, 'r') as f:
            lines = f.readlines()

        # Iterate through the lines
        for line in lines:
            # Check if the line includes "def" or "class"
            if not "default" in line and ("def" in line or "class" in line):
                if "def" in line:
                    matching_lines.append(line[4:-1])
                elif "class" in line:
                    call_pattern = re.compile(r':')
                    line = call_pattern.sub('()', line)
                    matching_lines.append(line[6:-1])

    # Return the list of matching lines
    return matching_lines


def clean_results(original_strings):
    # Compile a regular expression pattern to match "self" or " -> WebElement"
    self_pattern = re.compile(r'\bself, \b|\bself\b')
    web_element_pattern = re.compile(r'\).*')
    def_pattern = re.compile(r'\bdef \b')
    # Iterate through the strings in the list
    for i, s in enumerate(original_strings):
        # Use the regex pattern to replace "self" and " -> WebElement" with an empty string
        modified_string = self_pattern.sub('', s)
        # Use the regex pattern to replace " -> WebElement" with an empty string
        modified_string2 = web_element_pattern.sub(')', modified_string)
        modified_string3 = def_pattern.sub('', modified_string2)
        # Update the original string in the list with the modified string
        original_strings[i] = modified_string3

    # Return the modified list of strings
    return original_strings


def write_results(modified_strings):
    # Create the file if it doesn't exist
    if not os.path.exists('tests.py'):
        open('tests.py', 'w').close()
    else:
        # Delete the file "tests.py"
        os.remove("tests.py")
        open('tests.py', 'w').close()

    # Open the file in append mode
    with open('tests.py', 'a') as f:
        # Iterate through the modified strings
        for s in modified_strings:
            # Write the string to the file followed by a newline character
            f.write(s + '\n')


if __name__ == '__main__':
    # Get the path of the folder above the current folder
    # current_folder = os.path.dirname(os.path.abspath(__file__))
    current_folder = "C:\\Users\\danedens\\lab\\minimtestkit\\guitestkit\\Gui_Automation\\Page_Objects"

    # Find all lines that contain "def" or "class" in the parent folder
    original_strings = find_def_or_class(current_folder)
    # Clean the results by removing "self" and " -> WebElement"
    modified_strings = clean_results(original_strings)
    # Write the modified strings to the file
    write_results(modified_strings)
