Description
===========

*Please send me feedback and comments to carlitos.kyo@gmail.com*

Based on djbuild and code from setuptools used.

This buildout recipe can be used to create a setup for gae project. It will
automatically install apps into libs directory.

You can see an example of how to use the recipe below::

  [buildout]
  parts = satchmo gae
  eggs = ipython

  [satchmo]
  recipe = gocept.download
  url = http://www.satchmoproject.com/snapshots/satchmo-0.6.tar.gz
  md5sum = 659a4845c1c731be5cfe29bfcc5d14b1

  [gae]
  recipe = gaebuild
  settings = development
  eggs = ${buildout:eggs}
  project = dummyshop


Supported options
=================

The recipe supports the following options.

apps 
  projects that can be installed using pypi or compressed files. No handle
  dependencies do it by hand using buildout, the decision was taken for these reasons:
  
  * if dependency is a gae/django app this should be declared into this option to install
    it into the extarnal-apps directory or it should be omited if the dependency
    was customized and it is on local-apps directory
    
  * if dependency is not a gae/django app this should be declared into libs option.
  
  To delete an application should be by hand.

project
  This option sets the name for your project. The recipe will create a
  basic structure if the project is not already there.
  
external-apps
  This option sets the directory where external reusable apps goes. Which do not
  be installed as an egg or if you don't want install it as an egg.
  
local-apps
  This option sets the directory where local reusable apps goes, usually
  put the company name for this directory, and customized apps.

python
  This option can be used to specify a specific Python version which can be a
  different version from the one used to run the buildout.

settings
  You can set the name of the settings file which is to be used with
  this option. This is useful if you want to have a different
  production setup from your development setup. It defaults to
  `development`. if turboengine is setup

download-cache
  Set this to a folder somewhere on you system to speed up
  installation. The recipe will use this folder as a cache for a
  downloaded version of Django.

libs-path
  Path specified here will be used to install python projects
  
script-dir
  Paths specified here will be used to extend the default Python
  path for the `bin/*` scripts. default 'bin' some common scripts
  will be wsdl2py used for webservices and ZSI

find-links
  used to install apps inside the project
  
turboengine
  use turboengine set the version or 'last' for last version
  
webservices
  set true to use turboengines webservices wrapper, gaebuild will install ZSI 
  and zope.interface only avaible if turboengine is used, default false
  
libs
  pure python libraries to install into libs-dir, default lib
  
zipped
  true for install compressed eggs(libs) format or false as directory default false.

All following options only have effect when the project specified by
the project option has not been created already, on the setting file 
especified.

Notes.-

* If use turboengine don't edit app.py if generated authomaticaly by the recipe but Please
  edit webservices.py only generated once.
* If not edit app.py first extending pythonpath if you change this variables: local-apps, extarnal-apps
  libs-dir
* If some app or project has error on its setup.py file the process is terminated


Another example
===============

The next example shows you how to use some more of the options::

  [buildout]
  parts = gae extras
  eggs =
    hashlib

  [extras]
  recipe = iw.recipe.subversion
  urls =
    http://django-command-extensions.googlecode.com/svn/trunk/ django-command-extensions
    http://django-mptt.googlecode.com/svn/trunk/ django-mptt

  [gae]
  recipe = gaebuild
  settings = development
  project = exampleproject
  eggs =
    ${buildout:eggs}


Example with a different Python version
=======================================

To use a different Python version from the one that ran buildout in the
generated script use something like::

  [buildout]
  parts	= myproject

  [special-python]
  executable = /some/special/python

  [myproject]
  recipe	= gaebuild
  project	= myproject
  python	= special-python
