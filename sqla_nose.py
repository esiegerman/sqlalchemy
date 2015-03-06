#!/usr/bin/env python
"""
nose runner script.

This script is a front-end to "nosetests" which
installs SQLAlchemy's testing plugin into the local environment.

"""
import os
import re
import sys
import imp
import nose


from os import path
for pth in ['./lib']:
    sys.path.insert(0, path.join(path.dirname(path.abspath(__file__)), pth))

# installing without importing SQLAlchemy, so that coverage includes
# SQLAlchemy itself.
path = "lib/sqlalchemy/testing/plugin/noseplugin.py"
noseplugin = imp.load_source("noseplugin", path)

nose_ver = tuple(int(d) for d in re.findall(r'\d+', nose.__version__))
if nose_ver <= (0, 10, 4):
    # nose version 0.10.4 did not include the "addplugins"
    # option, so implement directly
    from nose.core import Config
    from nose.core import all_config_files
    from nose.plugins.manager import DefaultPluginManager

    class AddPluginManager(DefaultPluginManager):
        def loadPlugins(self):
            super(AddPluginManager, self).loadPlugins()
            self.addPlugin(noseplugin.NoseSQLAlchemy())

    manager = AddPluginManager()
    config = Config(
        env=os.environ,
        files=all_config_files(), plugins=manager)

    nose.main(config=config)
else:
    nose.main(addplugins=[noseplugin.NoseSQLAlchemy()])
