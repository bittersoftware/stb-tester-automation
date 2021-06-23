#!/usr/bin/env python2
import configparser
import imp
import logging
import os


class ModulePath:
    """Path to custom modules inside core"""

    config_file = "config.conf"
    network_capture = "network_capture.py"
    plot = "plot.py"


class ImportsUtils:
    """Reads from config.conf file the path for the utils in core

    Raises:
        OSError: Config file not found
        ImportError: Error in import

    Returns:
        cls: class module from core to instantiate
    """

    @staticmethod
    def get_module(path):
        logger = logging.getLogger(__file__)

        config = configparser.ConfigParser()

        cfg_path = (
            str(os.path.dirname(os.path.abspath(__file__)).split("utils")[0])
            + ModulePath.config_file
        )

        try:
            config.read(cfg_path)
        except Exception:
            raise OSError("Config file not found")

        utils_path = config.get("PATH", "UtilsPath")

        module = imp.load_source(path, "{}{}".format(utils_path, path))
        if module:
            return module
        else:
            logger.error("Module error in {}".format(path))
            raise ImportError


# Differents returns of classes of network_capture
def network_module():
    """Gets network module to perform real time analysis

    Returns:
        cls: class to instantiate
    """
    module = ImportsUtils.get_module(ModulePath.network_capture)
    return module


# Differents returns of classes of plot
def plot():
    """Gets plot module to create charts

    Returns:
        cls: class to instantiate
    """
    module = ImportsUtils.get_module(ModulePath.plot)
    return module
