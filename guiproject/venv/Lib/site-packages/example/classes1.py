### "imports"
from example.classes import Data

### "other-imports"
import csv
import json

from example.utils import tempdir

### "csv-subclass"
class Csv(Data):
    """
    CSV type.
    """
    aliases = ['csv']

    def present(self):
        with tempdir():
            with open("dictionary.csv", "w") as f:
                headers = list(self.data[0].keys())
                writer = csv.DictWriter(f, headers)

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

    def present(self):
        return json.dumps(self.data) 

