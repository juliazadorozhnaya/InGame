from doit.tools import run_once


DOIT_CONFIG = {'default_tasks': []}
#               ['docs', 'babel', 'tests']}


def task_flake8():
    """Run flake8"""
    return {
        'actions': ['flake8']
    }


def task_pydocstyle():
    """Run pydocstyle"""
    return {
        'actions': ['pydocstyle']
    }


def task_docs():
    """Create documentation in html."""
    return {
        'actions': ['make -C ./docs html']
    }


def task_babel():
    """Creates generative files for babel (Translation)"""
    return {
        'actions': ['pybabel compile -D ingame -d ./translation -l ru &&'
                    'pybabel compile -D ingame -d ./translation -l en &&']
    }


def task_tests():
    """Run tests"""
    return {
        'actions': ['''pytest ./tests/Tests.py''']
    }


def task_wheel():
    """Generates wheel distribution"""
    return {
        'actions': ['''python -m build -w'''],
        'task_dep': ["babel"]
    }
