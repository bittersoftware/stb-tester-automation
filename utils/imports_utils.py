#!/usr/bin/env python2
import configparser
import imp
import logging
import os
from enum import Enum


class Path(Enum):
    config_file = "config.conf"
    network_capture = "network_capture.py"
    plot = "plot.py"


class ImportsUtils:
    @staticmethod
    def get_module(path):
        logger = logging.getLogger(__file__)

        config = configparser.ConfigParser()

        cfg_path = (
            str(os.path.dirname(os.path.abspath(__file__)).split("utils")[0])
            + Path.config_file.value
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
    module = ImportsUtils.get_module(Path.network_capture.value)
    return module


# Differents returns of classes of plot
def plot():
    module = ImportsUtils.get_module(Path.plot.value)
    return module
