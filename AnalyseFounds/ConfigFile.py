# encoding: UTF-8
#
# Project: pyFinanceTool
# Author: borlittle
# CreateDate: 2017/11/19
"""
  BriefIntroduction:
    
    
  Update:
    
    
  Reference:
    
  RunningEnvironment: python 3.5 and above  
"""

# import packages
import logging

from backports import configparser


# class ConfigFile
class ConfigFile():
    def __init__(self, parent=None):

        self.conf = configparser.ConfigParser()
        self.configParamsDit = {}

    def readConfigParams(self, fileName='config.ini'):
        """
        read config params in config file
        :param fileName: the file name, default is congfig.ini
        :return: self.configParamsDit
        """
        try:
            self.configParamsDit = {}
            self.conf.read(filenames=fileName)
            sectionsList = self.conf.sections()
            if len(sectionsList) > 0:
                for each in sectionsList:
                    valuePair = self.conf.items(each)
                    value = {}
                    if len(valuePair) > 0:
                        for i in range(0, len(valuePair) - 1):
                            value[valuePair[i][0]] = valuePair[i][1]
                    self.configParamsDit[each] = value
                logging.info('read config file success')
        except Exception as e:
            logging.DEBUG(e)


# just for unit test
if __name__ == '__main__':
    conf = ConfigFile()
    conf.readConfigParams()
