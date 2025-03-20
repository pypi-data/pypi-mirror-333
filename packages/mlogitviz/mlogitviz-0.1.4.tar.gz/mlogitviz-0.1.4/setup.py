from setuptools import setup, find_packages

setup(
    name='mlogitviz',  # Your package name
    version='0.1.4',
    author='Payam Saeedi and Eric Williams',
    author_email='ps4019@rit.edu',
    description='A library to compute and visualize marginal effects for multinomial logistic regression models',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/payamv3/mlogitviz',  # Update with your repo URL
    packages=find_packages(),  # Automatically find the package folders
    install_requires=[
        'pandas',
        'numpy',
        'statsmodels',
        'matplotlib',
        'seaborn'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # or whichever license you choose
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
