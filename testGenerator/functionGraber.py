import ast
import os

class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, file_name, project_base_path):
        self.functions = []
        self.global_imports = {}
        self.current_function = None
        self.file_name = file_name
        self.project_base_path = project_base_path

    def visit_FunctionDef(self, node):
        function_info = {
            'name': node.name,
            'imports': set(),
            'code': ast.unparse(node),  # Get the function code as a string
            'module': self.file_name,  # Store the module/file name
            'model_definitions': {}  # Initialize model definitions
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
                import_name = self.global_imports[node.id]
                self.current_function['imports'].add(import_name)

                # Check if it's a model by looking for specific patterns
                if 'models' in import_name.split('.') and not import_name.endswith('.models'):
                    self.current_function['model_definitions'].update(
                        self.get_model_definitions([import_name])
                    )

        self.generic_visit(node)
        
    def get_model_definitions(self, models):
        model_definitions = {}
        for model in models:
            module_path, class_name = model.rsplit('.', 1)
            file_path = os.path.join(self.project_base_path, *module_path.split('.')) + '.py'
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    tree = ast.parse(file.read(), filename=file_path)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef) and node.name == class_name:
                        model_definitions[model] = ast.unparse(node)
            else:
                model_definitions[model] = f"# Error: Could not find model file for {model}"
        return model_definitions

def get_functions_and_imports(file_path, app_dir_name, project_base_path):

    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)

    app_dir_index = file_path.lower().index(app_dir_name.lower())
    relative_path = file_path[app_dir_index:]

    # Convert the relative path to a module path
    module_path = os.path.splitext(relative_path.replace(os.sep, '.'))[0]
    # Ensure no leading dots
    module_path = module_path.lstrip('.')

    visitor = FunctionVisitor(module_path, project_base_path)
    visitor.visit(tree)

    return visitor.functions

def format_function_as_string(func):
    func_name = func['name']
    func_code = func['code']
    imports = '\n  - '.join(func['imports'])
    import_statement = f"{func['module']}.{func_name}"
    model_defs = '\n\n'.join([f"{value}" for key, value in func['model_definitions'].items()])
    
    formatted_string = (
        f"Function Code:\n{func_code}\n\n"
        f"Modules and Imports:\n"
        f"- Function to Test: {import_statement}\n"
        f"- Dependencies:\n  - {imports}\n\n"
        f"Model Definitions:\n{model_defs}\n"
    )

    return formatted_string
