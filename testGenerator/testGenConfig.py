import os
project_root_module_name='app'

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source_dir = os.path.join(root_dir, 'app')

test_dir= os.path.join(root_dir, 'tests')