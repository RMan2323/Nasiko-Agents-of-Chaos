import os
import ast


def extract_functions_and_classes(file_path):
    """
    Extract classes, functions and their arguments from a python file
    """

    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    result = {
        "classes": {},
        "functions": {}
    }

    for node in ast.walk(tree):

        # Top-level functions
        if isinstance(node, ast.FunctionDef):
            args = [arg.arg for arg in node.args.args]
            result["functions"][node.name] = args

        # Classes
        elif isinstance(node, ast.ClassDef):

            methods = {}

            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    args = [arg.arg for arg in item.args.args]
                    methods[item.name] = args

            result["classes"][node.name] = methods

    return result


def analyze_project(src_dir):
    """
    Recursively analyze python files inside src_dir
    """

    project_data = {}

    for root, dirs, files in os.walk(src_dir):

        # ignore __pycache__
        dirs[:] = [d for d in dirs if d != "__pycache__"]

        for file in files:
            if file.endswith(".py"):

                file_path = os.path.join(root, file)

                try:
                    info = extract_functions_and_classes(file_path)
                    project_data[file_path] = info
                except Exception as e:
                    project_data[file_path] = {"error": str(e)}

    return project_data


def print_report(data):

    for file, content in data.items():

        print("\n" + "=" * 60)
        print("FILE:", file)

        # classes
        if content.get("classes"):
            print("\n  Classes:")
            for cls, methods in content["classes"].items():

                print(f"    class {cls}")

                for m, args in methods.items():
                    arg_str = ", ".join(args)
                    print(f"       -> {m}({arg_str})")

        # functions
        if content.get("functions"):
            print("\n  Functions:")
            for fn, args in content["functions"].items():

                arg_str = ", ".join(args)
                print(f"    {fn}({arg_str})")


if __name__ == "__main__":

    src_directory = "src"

    data = analyze_project(src_directory)

    print_report(data)