from setuptools import setup, find_packages

setup(
    name='flask-email-app',
    version='0.0.1',
    description='A simple email scheduling app built with Flask',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='vnpnh',
    author_email='no@email.com',
    url='https://github.com/vnpnh/flask-email-app',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
