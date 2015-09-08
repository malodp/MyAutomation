#!/usr/bin/python

import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read("test.ini")
print Config.sections()

