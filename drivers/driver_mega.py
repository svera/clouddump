from drivers.service import Service
import sys
import logging
import errno
import calendar
import datetime
try:
    from mega import Mega
except ImportError:
    print """Need Mega connection library! 
        (https://github.com/richardasaurus/mega.py)"""
    sys.exit(errno.ENOPKG)

'''
Implements Mega cloud-storage service interface to be used with Clouddump.
'''

class DriverMega(Service):

    ERROR_TRY_AGAIN = -3
    NODE_FILE       = 0
    NODE_ROOT       = 2


    def __init__(self, params):
        '''
        Connects to Mega with the provided credentials

        Arguments
        ---------
        params: A dict with the params to be passed to the initialised object
        '''

        self.logger = logging.getLogger('clouddump')
        self.logger.info("Connecting to Mega...")
        self.params = params
        self.mega = Mega()
        try:
            self.mega.login(params['user_name'], params['password'])
            self.logger.info("Sucessfully logged in to Mega.")
        except Exception:
            self.logger.error(
                "Authentication to Mega failed. Please check user / password.")
            sys.exit(errno.EPERM)


    def upload(self, file_name):
        '''
        Uploads the file to Mega, retrying if it couldn't be achieved

        Arguments
        ---------
        file_name: A string with the name of the file to be uploaded
        '''

        try:
            link = self._upload_try(file_name)
        except Exception as e:
            if e == DriverMega.ERROR_TRY_AGAIN:
                count = 0
                self.logger.warn(
                    "Failed to upload %s to Mega. Trying again..." %
                    (file_name))
                while link == None and count < self.params['retries']:
                    link = self._upload_try(file_name)
                    count += 1
                if link == None:
                    self.logger.error("Upload failed after all retries.")


    def delete_old_files(self):
        '''Delete files from the specified folder older than x days'''

        files = self._get_folder_files()
        if len(files) > 0:
            past = datetime.datetime.now() - datetime.timedelta(
                days = self.params["delete_files_older_than"])
            past_timestamp = calendar.timegm(past.utctimetuple())
            for file_id, file_metadata in files.iteritems():
                if file_metadata['ts'] < past_timestamp:
                    try:
                        self.mega.delete(file_id)
                        self.logger.info(
                            "%s deleted" % (file_metadata['a']['n']))
                    except Exception as e:
                        if e == DriverMega.ERROR_TRY_AGAIN:
                            self.logger.warn(
                                "Failed to delete %s from Mega." %
                                (file_metadata['a']['n']))

        else:
            self.logger.info("No files to delete")


    def _get_folder_files(self):
        '''
        Return the files stored in the specified folder, or from the root one
        if no folder was passed
        '''

        if self.params['folder_name'] == '':
            only_files = {}
            files = self.mega.get_files_in_node(DriverMega.NODE_ROOT)
            for key, value in files.iteritems():
                if value['t'] == DriverMega.NODE_FILE:
                    only_files[key] = value
            return only_files

        folder = self.mega.find(self.params['folder_name'])
        return self.mega.get_files_in_node(folder[0])


    def _upload_try(self, file_name):
        '''
        Uploads the file to the selected folder in Mega, or root if no
        folder was chosen

        Arguments
        ---------
        file_name: A string with the name of the file to be uploaded
        '''

        self.logger.info("Uploading %s..." % (file_name))
        if self.params['folder_name'] == '':
            file = self.mega.upload(file_name)
        else:
            folder = self.mega.find(self.params['folder_name'])
            if folder:
                file = self.mega.upload(file_name, folder[0])
            else:
                self.logger.critical("Folder %s doesn't exists in Mega." %
                                    (self.params['folder_name']))
                sys.exit(errno.ENOENT)
        return self.mega.get_upload_link(file)
