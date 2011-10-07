import os

from setuptools import setup, find_packages

version = '0.2.4'

def read_file(name):
    return open(os.path.join(os.path.dirname(__file__),
                             name)).read()

readme = read_file('README.txt')
# changes = read_file('CHANGES.txt')

setup(name='gaebuild',
      version=version,
      description="Buildout recipe for Google app engine",
      long_description=readme,
      classifiers=[
        'Framework :: Buildout',
        'Topic :: Software Development :: Build Tools',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        ],
      package_dir={'': 'src'},
      packages=find_packages('src'),
      keywords='',
      author='Luis C. Cruz',
      author_email='carlitos.kyo@gmail.com',
      url='https://github.com/carlitux/gaebuild',
      license='BSD',
      zip_safe=False,
      install_requires=[
        'zc.buildout',
        'zc.recipe.egg',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [zc.buildout]
      default = gaebuild:GAEBuild
      """,
      )
