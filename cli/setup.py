from setuptools import setup

setup(
    name = "chaos_cli",
    version = "0.1",
    install_requieres = ["Click","requests",],
    py_modules = ['chaos_cli'],
    entry_points = '''
    [console_scripts]
    chaos=chaos_cli:cli_main
    '''

)