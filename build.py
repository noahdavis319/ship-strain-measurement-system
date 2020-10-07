#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init, task, Author

use_plugin('python.core')
use_plugin('python.unittest')
use_plugin('python.coverage')
use_plugin('python.distutils')
use_plugin('python.pycharm')
use_plugin('python.install_dependencies')
use_plugin('python.sphinx')


name = 'SSMS'
default_task = ('install_dependencies', 'install')


@init
def set_properties(project):
    project.build_depends_on('sphinx')

    project.depends_on('imutils')
    project.depends_on('opencv-python-headless')
    project.depends_on('PyQt5')

    project.set_property('distutils_console_scripts', ['ssms=ssms.cli:cli'])

    project.set_property('coverage_threshold_warn', 90)
    project.set_property('coverage_branch_threshold_warn', 90)
    project.set_property('coverage_branch_partial_threshold_warn', 90)
    project.set_property('coverage_break_build', False)

    project.set_property('sphinx_doc_author', 'Noah Davis')
    project.set_property('sphinx_doc_builder', 'html')
    project.set_property('sphinx_project_name', project.name)
    project.set_property('sphinx_project_version', project.version)
    project.set_property('sphinx_config_path', 'src/docs')
    project.set_property('sphinx_source_dir', 'src/docs')
    project.set_property('sphinx_output_dir', 'target/docs')


@task()
def install_dependencies():
    pass
