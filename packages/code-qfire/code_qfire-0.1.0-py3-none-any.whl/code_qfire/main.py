import re
import argparse
from termcolor import colored

def read_file(file_path):
    """Reads a file and returns its content as a list of lines."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError:
        print(colored(f"❌ Error: File '{file_path}' not found.", "red"))
        return []

def print_warning(message):
    """Prints a formatted warning message without Unicode issues."""
    print(colored(f"\n[WARNING] {message}", "yellow"))

def print_suggestion(message):
    """Prints a formatted suggestion message without Unicode issues."""
    print(colored(f"[SUGGESTION] {message}", "green"))


def detect_nested_loops(code_lines):
    """Detects nested loops in the code."""
    loop_pattern = re.compile(r"\bfor\b|\bwhile\b")
    loop_stack = []
    results = []

    for i, line in enumerate(code_lines, start=1):
        if loop_pattern.search(line):
            loop_stack.append(i)
            if len(loop_stack) > 1:
                message = f"Nested loop found at line {i}"
                suggestion = "Consider optimizing or using a hashmap."
                print_warning(message)
                print_suggestion(suggestion)
                results.append(f"{message}\n{suggestion}\n")

    return results

def detect_unused_variables(code_lines):
    """Finds unused variables."""
    variables_declared = {}
    variables_used = set()
    results = []

    for i, line in enumerate(code_lines, start=1):
        match = re.search(r"\b(\w+)\s*=", line)
        if match:
            variable = match.group(1)
            variables_declared[variable] = i

        for variable in variables_declared.keys():
            if variable in line:
                variables_used.add(variable)

    unused_vars = set(variables_declared.keys()) - variables_used
    for var in unused_vars:
        message = f"Unused variable '{var}' declared at line {variables_declared[var]}"
        print_warning(message)
        results.append(message)

    return results

def detect_slow_sql_queries(code_lines):
    """Detects unoptimized SQL queries like 'SELECT * FROM'."""
    results = []
    for i, line in enumerate(code_lines, start=1):
        if re.search(r"SELECT \*", line, re.IGNORECASE):
            message = f"Unoptimized SQL query at line {i}"
            suggestion = "Use 'SELECT column_name' instead of 'SELECT *'."
            print_warning(message)
            print_suggestion(suggestion)
            results.append(f"{message}\n{suggestion}\n")
    return results

def save_report(results, file_path="report.txt"):
    """Saves warnings and suggestions to a report file with UTF-8 encoding."""
    with open(file_path, "w", encoding="utf-8") as f:
        for line in results:
            f.write(line + "\n")
    print(colored(f"\n📄 Report saved to {file_path}", "cyan"))

def main():
    """Main function to run CODE-QFIRE from CLI."""
    parser = argparse.ArgumentParser(description="CODE-QFIRE Code Optimizer")
    parser.add_argument("-v", "--version", action="version", version="CODE-QFIRE 0.1.0")
    parser.add_argument("file", nargs="?", help="File to scan for inefficiencies")

    args = parser.parse_args()

    code_lines = read_file(args.file)
    results = []
    results.append(f"🔍 CODE-QFIRE Optimization Report for {args.file}\n")

    results.extend(detect_nested_loops(code_lines))
    results.extend(detect_unused_variables(code_lines))
    results.extend(detect_slow_sql_queries(code_lines))

    save_report(results)

if __name__ == "__main__":
    main()