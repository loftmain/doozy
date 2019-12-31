import pprint 

### "import"
from example.classes import Data

### "plugins"
Data.plugins
import example.classes2
Data.plugins

### "example-data"
example_data = [{
    "foo" : 123,
    "bar" : 456
    }]

### "csv-example"
csv_data = Data.create_instance('csv', example_data)

csv_data.present()

csv_data.update_settings({
    'lineterminator' : '\n',
    'write_header' : False
    })

csv_data.present()

csv_data.setting('lineterminator')

pprint.pprint(csv_data.setting_values())

### "json-example"
json_data = Data.create_instance('json', example_data)
json_data.present()
