from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='RaydiumPy',
      version='0.0.1',
      description='RaydiumPy',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/defipy-devs/raydiumpy',
      author = "icmoore",
      author_email = "defipy.devs@gmail.com",
      license='MIT',
      package_dir = {"raydiumpy": "python/prod"},
      packages=[
          'raydiumpy',
          'raydiumpy.erc'
      ],   
      zip_safe=False)
