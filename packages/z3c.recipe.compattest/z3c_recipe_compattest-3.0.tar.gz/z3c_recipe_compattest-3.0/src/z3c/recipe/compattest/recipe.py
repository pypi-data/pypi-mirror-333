import os
import re

import pkg_resources

import zc.buildout.easy_install
import zc.recipe.egg
import zc.recipe.testrunner


def string2list(string, default):
    result = string and string.split() or default
    return [item.strip() for item in result]


RUNNER_PREFIX = 'runner-'


class Recipe:

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options

        if 'max_jobs' not in options:
            options['max_jobs'] = '1'

        self.include = string2list(self.options.get('include', ''), [])
        self.exclude = string2list(self.options.get('exclude', ''), [])
        self.extra_paths = self.options.get('extra-paths', '')

        self.script = self.options.get('script', self.name)

        # gather options to be passed to the underlying testrunner
        self.testrunner_options = {}

        for opt in self.options:
            if opt.startswith(RUNNER_PREFIX):
                runner_opt = opt[len(RUNNER_PREFIX):]
                self.testrunner_options[runner_opt] = self.options[opt]

    def install(self):
        return self.update()

    def update(self):
        wanted_packages = self._wanted_packages()
        installed = []
        installed.extend(self._install_testrunners(wanted_packages))
        installed.extend(self._install_run_script(wanted_packages))
        return installed

    def _install_testrunners(self, wanted_packages):
        installed = []
        for package_name in wanted_packages:
            ws = self._working_set(package_name)
            package = ws.find(pkg_resources.Requirement.parse(package_name))
            # Installing arbitrary extras here leads to problems in
            # reproducibility.
            # In particular, setuptools[tests] causes a huge dependency tree
            # to be brought in.
            extras = '[{}]'.format(
                ','.join(ex for ex in package.extras if ex in ['test']))
            if package_name == 'zc.buildout':
                # Installing the test dependencies for zc.buildout is also a
                # problem, they don't all provide test extras
                extras = ''
            options = self.testrunner_options.copy()
            options['eggs'] = package_name + extras
            print("Installing", options['eggs'])
            if self.extra_paths:
                options['extra-paths'] = self.extra_paths

            recipe = zc.recipe.testrunner.TestRunner(
                self.buildout, f'{self.name}-{package_name}', options)
            installed.extend(recipe.install())
        return installed

    def _install_run_script(self, wanted_packages):
        bindir = self.buildout['buildout']['bin-directory']
        runners = [f'{self.name}-{package}' for package
                   in wanted_packages]
        runners = [repr(os.path.join(bindir, runner)) for runner in runners]

        return zc.buildout.easy_install.scripts(
            [(self.script, 'z3c.recipe.compattest.runner', 'main')],
            self._working_set('z3c.recipe.compattest'),
            self.buildout['buildout']['executable'],
            bindir, arguments='{}, {}'.format(self.options['max_jobs'],
                                              ', '.join(runners)))

    def _wanted_packages(self):
        projects = list(set(self.include))  # Filter out duplicates.
        for project in projects:
            for regex in self.exclude:
                if re.compile(regex).search(project):
                    projects.remove(project)
                    break
        return projects

    def _working_set(self, package):
        eggs = zc.recipe.egg.Egg(self.buildout, self.name, dict(eggs=package))
        _, ws = eggs.working_set()
        return ws
