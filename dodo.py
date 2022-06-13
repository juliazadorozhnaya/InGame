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
    """Make HTML documentation."""
    return {
        'actions': ['make -C ./docs html']
    }


def task_translation():
    """Create generative files for babel"""
    return {
        'actions': ['pybabel compile -D ingame -d ./translation -l ru &&'
                    'pybabel compile -D ingame -d ./translation -l en']
    }


def task_tests():
    """Run tests"""
    return {
        'actions': ['''python3 tests/tests.py''']
    }


def task_wheel():
    """Generates wheel distribution"""
    return {
        'actions': ['rm -rf dist build',
                    'rm -rf build *.egg-info',
                    'pip3 install build -U',
                    'python3 -m build',
                    'pip3 install dist/ingame-0.0.1-py3-none-any.whl'],
        'task_dep': ["translation"]
    }
