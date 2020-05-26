from setuptools import setup, find_packages

setup(
    name='songlibrary',
    version='1.0',
    author='Alana Quinones Garcia',
    author_email='lana47879@gmail.com',
    description='CLI that provides easy access to study materials for songs',
    packages=find_packages(),
    include_package_data=True,
    py_modules=['songlib'],
    install_requires=[
        'Click',
        'validators',
    ],
    entry_points={
        'console_scripts': [
            'songlib = songlib.songlib:cli',
        ],
    },
)
