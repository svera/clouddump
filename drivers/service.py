from abc import ABCMeta, abstractmethod

'''
Abstract class that defines the necessary methods
that should be implemented when defining a cloud-storage
service to be used with backupper
'''

class Service(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        '''Connects to the cloud service'''

    @abstractmethod
    def upload(self):
        '''Uploads the passed file to the service '''

    @abstractmethod
    def delete_old_files(self):
        '''Deletes old files from the service '''        