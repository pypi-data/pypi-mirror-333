from setuptools import setup

APP = ['__init__.py']  # Replace with the name of your script
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': [],
    'plist': {
        'CFBundleName': "Eshaan's Mart",  # Custom app name for the dock
        'CFBundleIdentifier': "com.eshannmart.app",  # Unique identifier
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
