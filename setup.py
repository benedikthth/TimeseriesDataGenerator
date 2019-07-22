from setuptools import setup

setup(
   name='TimeseriesDataGenerator',
   version='1.0',
   description='Time series Data generator  ',
   author='Benedikt H. Thordarson',
   author_email='benediktt13@ru.is',
#    packages=['TimeseriesDataGenerator'],  #same as name
   istall_requires=['noise', 'numpy', 'random', 'timeit'], #external packages as dependencies
   scripts=[
            'TimeseriesDataGenerator.py',
           ]
)