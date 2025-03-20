from setuptools import setup, find_packages

setup(
    name='bot_pipeline',  # имя вашего пакета
    version='0.1.0',  # версия
    packages=find_packages(),
    install_requires=[
        'python-telegram-bot>=20.0',
	'requests>=2.20',
    ],
    author='Ivan',
    author_email='dmitrievivan434@gmail.com',
    description='bot',
    #long_description=open('README.md').read(),
    #long_description_content_type='text/markdown',
    #url='https://github.com/yourusername/my_package',  # URL вашего проекта
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
