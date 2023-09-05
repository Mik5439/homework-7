from setuptools import setup

setup(
    name='clean_folder',
    version='0.0.5',
    description='Folder sorted, cleaned',
    url='https://github.com/Mik5439/GoIT.git',
    author='Andrii Mikulskyi',
    author_email='andrii.mikulskyi@gmail.com',
    license='MIT',
    packages=['clean_folder'],
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
)