__author__ = 'chunlei3'

from django.core.files.uploadhandler import MemoryFileUploadHandler,StopUpload
from django.conf import settings

class MMFileUploadHandler(MemoryFileUploadHandler):

    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
        super(MMFileUploadHandler, self).handle_raw_input(input_data, META, content_length, boundary, encoding=None)
        if content_length > settings.MAX_FILEUPLOAD_SIZE:
            self.fileStop = True
        else:
            self.fileStop = False


    def new_file(self, *args, **kwargs):
        super(MMFileUploadHandler, self).new_file(*args, **kwargs)

    def receive_data_chunk(self, raw_data, start):
        if self.fileStop:
            return None
        return super(MMFileUploadHandler, self).receive_data_chunk(raw_data,start)

