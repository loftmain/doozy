### "imports"
from example.classes import Data

### "other-imports"
from example.utils import tempdir
import csv
import json

### "csv-subclass"
class Csv(Data):
    """
    CSV type.
    """
    aliases = ['csv']

    ### "csv-settings"
    _settings = {
            'write-header' : ("Whether to write a header row first.", True),

            'csv-settings' : (
                "List of settings which should be passed to python csv library.",
                ['dialect', 'delimiter', 'lineterminator']),

            'dialect' : ("CSV dialect.", None),
            'delimiter' : ("A one-character string used to separate fields.", None),
            'lineterminator' : ("String used to terminate lines.", None)
            }

    ### "list-dialects"
    def list_dialects(self):
        return csv.list_dialects()

    ### "csv-present"
    def present(self):
        kwargs = dict((k, v)
                for k, v in self.setting_values().items()
                if v and (k in self.setting('csv-settings'))
                )

        with tempdir():
            with open("dictionary.csv", "w") as f:
                writer = csv.DictWriter(f, list(self.data[0].keys()), **kwargs)

                if self.setting('write-header'):
                    writer.writeheader()

                writer.writerows(self.data)

            with open("dictionary.csv", "r") as f:
                return f.read()

### "json-subclass"
class Json(Data):
    """
    JSON type.
    """
    aliases = ['json']

    _settings = {
            }

    def present(self):
        return json.dumps(self.data) 
