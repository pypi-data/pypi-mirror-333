from setuptools import setup, find_packages

setup(
    name='pydoubao',
    version='0.1.3',
    author='Wenhao Liu',
    author_email='me@liuwenhao.me',
    description='Use doubao web api to build a chatbot, without using doubao API which need token fee.',
    long_description=open('README.md',encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://pypi.org/project/pydoubao/',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests'
    ],
)


