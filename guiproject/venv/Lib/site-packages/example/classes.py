### "imports"
from cashew import Plugin, PluginMeta

### "create-plugin-base-class"
class Data(Plugin, metaclass=PluginMeta):
    """
    Base class for plugins which present data in various ways.
    """

    ### "methods"
    def __init__(self, data):
        self.data = data

    def present(self):
        raise Exception("not implemented")
