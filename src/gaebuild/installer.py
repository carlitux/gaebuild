import os
import re
import shutil
import urllib2
import templates
import setuptools
import subprocess
import zc.recipe.egg

from zc.buildout import UserError
from dist_installer import install

class Installer:

    def __init__(self, options, buildout, log, name):
        self.options = options
        self.buildout = buildout
        self.log = log
        self.name = name

    def get_extra_paths(self):
        basic_dir = os.path.join(self.buildout['buildout']['directory'], 'src')
        local_apps_dir = os.path.join(basic_dir, self.options['project'], self.options['local-apps'])
        external_apps_dir = os.path.join(basic_dir, self.options['project'], self.options['external-apps'])
        extra_paths = [self.options['location'],
                       self.buildout['buildout']['directory'],
                       local_apps_dir, external_apps_dir]

        pythonpath = [p.replace('/', os.path.sep) for p in
                      self.options['libs-path'].splitlines() if p.strip()]

        extra_paths.extend(pythonpath)

        return extra_paths

    def command(self, cmd, **kwargs):
        output = subprocess.PIPE
        if self.buildout['buildout'].get('verbosity'):
            output = None
        command = subprocess.Popen(
            cmd, shell=True, stdout=output, **kwargs)
        return command.wait()

    def create_file(self, file, template, options=None):
        f = open(file, 'w')
        if options is not None:
            f.write(template % options)
        else:
            f.write(template)
        f.close()

    def make_scripts(self, location, extra_paths, ws):
        scripts = []
        if self.options['turboengine'] != '':
            self.create_file(os.path.join(location, self.options['project'],'app.py'), templates.configs['turboengine']['app_py'], {'local': self.options['local-apps'],
                                                                                                                                    'external': self.options['external-apps'],
                                                                                                                                    'lib': self.options['libs-path'],
                                                                                                                                    'settings': self.options['settings']})
        return scripts

    def create_project(self, project_dir, project):
        old_config = self.buildout._read_installed_part_options()[0]
        if self.name in old_config:
            old_config = old_config[self.name]

            if 'project' in old_config and\
               old_config['project'] != self.options['project']:
                self.log.warning("GAEBuild: creating new project '%s', to replace previous project '%s'"%(self.options['project'], old_config['project']))

        # saving current work directory
        old_cwd = os.getcwd()
        os.chdir(project_dir)

        # importing current django instalation
        os.makedirs(project)
        os.chdir(project)

        os.makedirs('docs')

        os.makedirs('static/css')
        os.makedirs('static/js')
        os.makedirs('static/images')

        os.makedirs('templates')
        os.makedirs('i18n')

        self.create_file("templates/base.html", templates.base_html)
        self.create_file("templates/404.html", templates.t_404_html)
        self.create_file("templates/500.html", templates.t_500_html)

        self.create_file("app.yaml", templates.configs['common']['app_yaml'], {})
        self.create_file("index.yaml", templates.configs['common']['index_yaml'], {})
        self.create_file("cron.yaml", templates.configs['common']['cron_yaml'], {})
        self.create_file("queue.yaml", templates.configs['common']['queue_yaml'], {})
        self.create_file("dos.yaml", templates.configs['common']['dos_yaml'], {})

        if self.options['turboengine'] == '':
            self.create_file("app.py", templates.configs['gae']['app_py'], {'local': self.options['local-apps'],
                                                                            'external': self.options['external-apps'],
                                                                            'lib':self.options['libs-path']})

        if self.options['turboengine'] != '':
            os.makedirs('project')
            self.create_file('project/__init__.py', '', {})

            self.create_file("settings.py", '# Customize here settings', {})
            self.create_file("project/development.py", templates.development_settings, {})
            self.create_file("project/production.py", templates.production_settings, {})

            if self.options['webservices'].lower() == 'true':
                self.create_file("webservices.py", templates.configs['turboengine']['webservices_py'], {'local': self.options['local-apps'],
                                                                                                        'external': self.options['external-apps'],
                                                                                                        'lib':self.options['libs-path']})

        # updating to original cwd
        os.chdir(old_cwd)

    def update_project_structure(self):
        old_config = self.buildout._read_installed_part_options()[0]
        # updating old config to project name
        if self.name in old_config:
            old_config = old_config[self.name]

            if 'local-apps' in old_config and\
               old_config['local-apps'] != self.options['local-apps']:
                if os.path.exists(old_config['local-apps']):
                    self.log.info("GAEBuild: moving local-apps dir from % to %s"%(old_config['local-apps'], self.options['local-apps']))
                    shutil.move(old_config['local-apps'], self.options['local-apps'])

            if 'external-apps' in old_config and\
               old_config['external-apps'] != self.options['external-apps']:
                if os.path.exists(old_config['external-apps']):
                    self.log.info("GAEBuild: moving external-apps dir from % to %s"%(old_config['external-apps'], self.options['external-apps']))
                    shutil.move(old_config['external-apps'], self.options['external-apps'])

            if 'libs-path' in old_config and\
               old_config['libs-path'] != self.options['libs-path']:
                if os.path.exists(old_config['libs-path']):
                    self.log.info("GAEBuild: moving libs-path dir from % to %s"%(old_config['libs-path'], self.options['libs-path']))
                    shutil.move(old_config['libs-path'], self.options['libs-path'])

            if 'script-dir' in old_config and\
               old_config['script-dir'] != self.options['script-dir']:
                if os.path.exists(old_config['script-dir']):
                    self.log.info("GAEBuild: moving script-dir dir from % to %s"%(old_config['script-dir'], self.options['script-dir']))
                    shutil.move(old_config['script-dir'], self.options['script-dir'])

        if not os.path.exists(self.options['local-apps']):
            self.log.info("GAEBuild: creating local-apps dir %s"%(self.options['local-apps']))
            os.makedirs(self.options['local-apps'])

        if not os.path.exists(self.options['external-apps']):
            self.log.info("GAEBuild: creating external-apps dir %s"%(self.options['external-apps']))
            os.makedirs(self.options['external-apps'])

        if not os.path.exists(self.options['libs-path']):
            self.log.info("GAEBuild: creating libs-path dir %s"%(self.options['libs-path']))
            os.makedirs(self.options['libs-path'])

        answer = raw_input("Do you want to install/update apps?(yes/no): ")

        if answer.lower() == 'yes':
            print '\n************** Intalling gae/django apps **************\n'
            apps = self.options.get('apps', '').split()
            if len(apps) == 0:
                self.log.info('No apps to install')
            else:
                install_dir = os.path.abspath(self.options['external-apps'])

                args = ['-U', '-b', self.buildout['buildout']['download-cache'], '-d', install_dir]
                args.extend(apps)

                links = self.options.get('find-links', '').split()

                if len(links)>0:
                    links.insert(0, '-f')
                    args.extend(links)

                install(args)
            print '\n************** End intalling gae/django apps **************\n'

            print '\n************** Intalling python projects **************\n'

            apps = self.options.get('libs', '').split()
            turboengine = self.options.get('turboengine', '')
            if turboengine != '':
                if turboengine.lower() == 'last' :
                    apps.append("turboengine")
                else:
                    apps.append("turboengine==%s"%self.options.get('turboengine'))
                if self.options.get('webservices').lower() == 'true':
                    apps.append("ZSI")
                    apps.append("zope.interface")

            if len(apps) == 0:
                self.log.info('No apps to install')
            else:
                from setuptools.command.easy_install import main
                install_dir = os.path.abspath(self.options['libs-path'])

                if self.options.get('zipped').lower() == 'true':
                    args = ['-U', '-z', '-d', install_dir]
                else:
                    args = ['-U', '-d', install_dir]

                args.extend(['-s', self.options['script-dir']])
                links = self.options.get('find-links', '').split()

                if len(links)>0:
                    links.insert(0, '-f')
                    args.extend(links)

                args.extend(apps)
                previous_path = os.environ.get('PYTHONPATH', '')
                if previous_path == '':
                    os.environ['PYTHONPATH'] = '%s'%(install_dir)
                else:
                    os.environ['PYTHONPATH'] = '%s:%s'%(install_dir, previous_path)

                main(args)# installing libs

                if previous_path == '':
                    del os.environ['PYTHONPATH']
                else:
                    os.environ['PYTHONPATH'] = previous_path

            print '\n************** End intalling python projects **************\n'

    def verify_or_create_download_dir(self, download_dir):
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)

    def install_recipe(self, location):
        self.options['setup'] = location
        development = zc.recipe.egg.Develop(self.buildout,
                                            self.options['recipe'],
                                            self.options)

        #development.install()
        del self.options['setup']

    def install_project(self, project_dir, project):
        if not os.path.exists(os.path.join(project_dir, project)):
            self.create_project(project_dir, project)
        else:
            self.log.info(
                'Skipping creating of project: %(project)s since '
                'it exists' % self.options)

        # creating structure
        old_cwd = os.getcwd()
        os.chdir(os.path.join(project_dir, project))

        self.update_project_structure()

        os.chdir(old_cwd)

    def install_scripts(self, location, extra_path, ws):
        script_paths = []

        # Make the wsgi and fastcgi scripts if enabled
        script_paths.extend(self.make_scripts(location, extra_path, ws))

        return script_paths
