from unittest import TestCase
from distutils.sysconfig import get_python_lib
from yapsy.PluginManager import PluginManager
from OpenMesher.interfaces import IOpenMesherConfigPlugin, IOpenMesherPackagePlugin, IOpenMesherDeployPlugin

class TestPlugins(TestCase):
    def test_plugins_found(self):
        pm = PluginManager()

        libpath = '%s/OpenMesher/plugins' % (get_python_lib())

        pm.setPluginPlaces([
            '/usr/share/openmesher/plugins',
            '~/.openmesher/plugins',
            './OpenMesher/plugins',
            './plugins',
            libpath,
        ])
        pm.setPluginInfoExtension('plugin')
        pm.setCategoriesFilter({
            'config': IOpenMesherConfigPlugin,
            'package': IOpenMesherPackagePlugin,
            'deploy': IOpenMesherDeployPlugin,
        })
        pm.collectPlugins()
        for plugin in pm.getAllPlugins():
            print('Author: %s' % (plugin.author))
            print('Categories: %s' % (plugin.categories))
            print('Copyright: %s' % (plugin.copyright))
            print('Descr: %s' % (plugin.description))
            print('Error: %s' % (plugin.error))
            print('Name: %s' % (plugin.name))
            print('Path: %s' % (plugin.path))
            print('Version: %s' % (plugin.version))
            print('Website: %s' % (plugin.website))
            print('')
        return True
