
import os

from django.conf import settings

class HandleFile(object):
    """This class handle with the file upload for multiple backends
    """
    def __init__(self, wrapper):
        self._handler_wrapper = wrapper

    def handle_file(self, f):
        """
        Handle File
        """
        self._handler_wrapper.handle_uploaded_file(f)

        # Store the metadata   

class FileSystemHandleFile(object):
    """Store the file in file system
    """
    def __init__(self):
        pass

    def handle_uploaded_file(self, f):
        """Store the files in file disk 
        """

        with open(os.path.join(os.path.abspath(settings.PROJECT_DIR_ROOT + 'emif/static/files/'), f.name),
                  'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

class MongoDBHandleFile(object):
    """Store the file in MongoDB
    """
    def __init__(self):
        pass

    def handle_uploaded_file(self, f):
        """Store the files in file disk 
        """
        pass

