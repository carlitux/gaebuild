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

libs-dir
  All paths specified here will be used to extend the default Python
  path for the `bin/*` scripts.

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


Another example
===============

The next example shows you how to use some more of the options::

  [buildout]
  parts = django extras
  eggs =
    hashlib

  [extras]
  recipe = iw.recipe.subversion
  urls =
    http://django-command-extensions.googlecode.com/svn/trunk/ django-command-extensions
    http://django-mptt.googlecode.com/svn/trunk/ django-mptt

  [django]
  recipe = djbuild
  version = trunk
  settings = development
  project = exampleproject
  wsgi = true
  eggs =
    ${buildout:eggs}
  test =
    someapp
    anotherapp

Example using .pth files
========================

Pinax uses a .pth file to add a bunch of libraries to its path; we can
specify it's directory to get the libraries it specified added to our
path::

  [buildout]
  parts	= PIL
	  svncode
	  myproject

  [PIL]
  recipe	= zc.recipe.egg:custom
  egg		= PIL
  find-links	= http://dist.repoze.org/

  [svncode]
  recipe	= iw.recipe.subversion
  urls		= http://svn.pinaxproject.com/pinax/tags/0.5.1rc1	pinax

  [myproject]
  recipe	= djbuild
  version	= 1.0.2
  eggs		= PIL
  project	= myproject
  settings	= settings
  extra-paths	= ${buildout:directory}/myproject/apps
		  ${svncode:location}/pinax/apps/external_apps
		  ${svncode:location}/pinax/apps/local_apps
  pth-files	= ${svncode:location}/pinax/libs/external_libs
  wsgi		= true

Above, we use stock Pinax for pth-files and extra-paths paths for
apps, and our own project for the path that will be found first in the
list.  Note that we expect our project to be checked out (e.g., by
svn:external) directly under this directory in to 'myproject'.

Example with a different Python version
=======================================

To use a different Python version from the one that ran buildout in the
generated script use something like::

  [buildout]
  parts	= myproject

  [special-python]
  executable = /some/special/python

  [myproject]
  recipe	= djbuild
  version	= 1.0.2
  project	= myproject
  python	= special-python


Example configuration for mod_wsgi
==================================

If you want to deploy a project using mod_wsgi you could use this
example as a starting point::

  <Directory /path/to/buildout>
         Order deny,allow
         Allow from all
  </Directory>
  <VirtualHost 1.2.3.4:80>
         ServerName      my.rocking.server
         CustomLog       /var/log/apache2/my.rocking.server/access.log combined
         ErrorLog        /var/log/apache2/my.rocking.server/error.log
         WSGIScriptAlias / /path/to/buildout/bin/django.wsgi
  </VirtualHost>
