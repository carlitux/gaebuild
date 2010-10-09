import logging, os, zc.buildout
import os

from installer import Installer

class GAEBuild(object):

    def __init__(self, buildout, name, options):
        self.log = logging.getLogger(name)
        self.egg = zc.recipe.egg.Egg(buildout, options['recipe'], options)

        self.buildout, self.name, self.options = buildout, name, options
        options['location'] = os.path.join(
            buildout['buildout']['parts-directory'], name)
        options['bin-directory'] = buildout['buildout']['bin-directory']

        options.setdefault('project', 'example.com')
        options.setdefault('external-apps', 'apps')
        options.setdefault('local-apps', 'company')
        options.setdefault('settings', 'development')
        options.setdefault('libs-path', 'lib')
        options.setdefault('script-dir', 'bin')
        options.setdefault('turboengine', '')
        options.setdefault('webservices', 'false')
        options.setdefault('zipped', 'false')

        # Usefull when using archived versions
        buildout['buildout'].setdefault(
            'download-cache',
            os.path.join(buildout['buildout']['directory'],
                         'downloads'))
        
        self.__installer = Installer(self.options, self.buildout, self.log, self.name)


    def install(self):
        print '\n------------------ Installing GAEBuild ------------------\n'
        location = self.options['location']
        base_dir = self.buildout['buildout']['directory']
        project_dir = os.path.join(base_dir, 'src')
        download_dir = self.buildout['buildout']['download-cache']
        
        extra_path = self.__installer.get_extra_paths()
        requirements, ws = self.egg.working_set(['gaebuild'])
        
        self.__installer.verify_or_create_download_dir(download_dir)
        
        self.__installer.install_recipe(location)
        self.__installer.install_project(project_dir, self.options['project'])
        
        script_paths = self.__installer.install_scripts(project_dir, extra_path, ws)
        
        print '\n------------------ Installing GAEBuild ------------------\n'

        return script_paths + [location]

    def update(self):
        pass
    