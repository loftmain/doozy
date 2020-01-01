import os
import shutil
import tempfile

class tempdir(object):
    def make_temp_dir(self):
        self.tempdir = tempfile.mkdtemp()
        self.location = os.path.abspath(os.curdir)
        os.chdir(self.tempdir)

    def remove_temp_dir(self):
        os.chdir(self.location)
        try:
            shutil.rmtree(self.tempdir)
        except Exception as e:
            print(e)
            print(f"was not able to remove tempdir '{self.tempdir}'")

    def __enter__(self):
        self.make_temp_dir()

    def __exit__(self, type, value, traceback):
        if not isinstance(value, Exception):
            self.remove_temp_dir()
