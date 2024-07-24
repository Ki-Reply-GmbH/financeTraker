import ast
import os

class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, file_name):
        self.functions = []
        self.global_imports = {}
        self.current_function = None
        self.file_name = file_name

    def visit_FunctionDef(self, node):
        function_info = {
            'name': node.name,
            'imports': set(),
            'code': ast.unparse(node),  # Get the function code as a string
            'module': self.file_name  # Store the module/file name
        }
        self.current_function = function_info

        self.generic_visit(node)

        self.functions.append(function_info)
        self.current_function = None

    def visit_Import(self, node):
        for alias in node.names:
            self.global_imports[alias.asname or alias.name] = alias.name
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module
        for alias in node.names:
            full_name = f"{module}.{alias.name}" if module else alias.name
            self.global_imports[alias.asname or alias.name] = full_name
        self.generic_visit(node)

    def visit_Name(self, node):
        if self.current_function is not None:
            if node.id in self.global_imports:
                self.current_function['imports'].add(self.global_imports[node.id])
        self.generic_visit(node)

def get_functions_and_imports(file_path, project_base_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)

    relative_path = os.path.relpath(file_path, project_base_path)
    module_path = os.path.splitext(relative_path.replace(os.sep, '.'))[0]

    # Ensure no leading dots
    module_path = module_path.lstrip('.')

    visitor = FunctionVisitor(module_path)
    visitor.visit(tree)

    return visitor.functions

def format_functions_as_string(functions):
    result = []
    for func in functions:
        func_name = func['name']
        func_code = func['code']
        imports = ', '.join(func['imports'])
        import_statement = f"from {func['module']} import {func_name}"
        result.append(f"Function Name: {func_name}\nFunction Code:\n{func_code}\nModules Used: {imports}\nImport Statement: {import_statement}\n")

    return result