# CloudWatchLogs Logging
# Copyright 2015 Immobilien Scout GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pybuilder.core import use_plugin, init, Author

use_plugin('python.core')
use_plugin('python.install_dependencies')
use_plugin('python.distutils')
use_plugin('python.flake8')
use_plugin('python.unittest')
use_plugin('python.coverage')

use_plugin('copy_resources')

default_task = ['analyze', 'publish']

name = 'python-cloudwatchlogs-logging'
version = '0.0.4'
summary = 'Handler for easy logging to AWS CloudWatchLogs.'
description = """
    Handler for easy logging to AWS CloudWatchLogs.
"""
authors = [Author('Arne Hilmann', 'arne.hilmann@gmail.com')]
url = 'https://github.com/ImmobilienScout24/python-cloudwatchlogs-logging'
license = 'Apache License 2.0'


@init
def set_properties(project):
    project.set_property("verbose", True)

    project.depends_on("docopt")
    project.depends_on("boto")

    project.build_depends_on("mock")

    project.set_property("flake8_include_test_sources", True)
    project.set_property('coverage_break_build', False)

    project.set_property("install_dependencies_upgrade", True)

    project.set_property('copy_resources_target', '$dir_dist')
    project.get_property('copy_resources_glob').append('setup.cfg')
    project.set_property('dir_dist_scripts', 'scripts')

    project.get_property('distutils_commands').append('bdist_egg')

    project.set_property('distutils_classifiers', [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python',
        'Topic :: System :: Networking',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Systems Administration'
    ])


@init(environments='teamcity')
def set_properties_for_teamcity_builds(project):
    import os
    project.version = '%s-%s' % (
        project.version, os.environ.get('BUILD_NUMBER', 0))
    project.default_task = ['install_build_dependencies', 'publish']
    project.set_property(
        'install_dependencies_index_url', os.environ.get('PYPIPROXY_URL'))
    project.set_property('install_dependencies_use_mirrors', False)
    project.set_property('teamcity_output', True)
