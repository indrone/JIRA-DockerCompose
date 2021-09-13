from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize('src/graph_fS_classification.py'))
setup(ext_modules = cythonize('src/balance_sheet_class.py'))
setup(ext_modules = cythonize('src/balance_sheet_graph.py'))
setup(ext_modules = cythonize('src/balance_sheet_rules.py'))
setup(ext_modules = cythonize('src/income_statement_class.py'))
setup(ext_modules = cythonize('src/cash_flow_class.py'))