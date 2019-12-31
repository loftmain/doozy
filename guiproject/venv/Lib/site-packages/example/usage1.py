### "import"
from example.classes import Data

### "plugins"
Data.plugins
import example.classes1
Data.plugins

### "example-data"
example_data = [{
    "foo" : 123,
    "bar" : 456
    }]

### "json-example-type"
json_data = Data.create_instance('json', example_data)
type(json_data)

### "csv-example"
csv_data = Data.create_instance('csv', example_data)
csv_data.present()

### "json-example"
json_data = Data.create_instance('json', example_data)
json_data.present()
