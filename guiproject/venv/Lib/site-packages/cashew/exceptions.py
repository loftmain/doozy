class CashewException(Exception):
    def __init__(self, message):
        self.message = message

class InternalCashewException(CashewException):
    pass

class UserFeedback(CashewException):
    pass

class InactivePlugin(UserFeedback):
    def __init__(self, plugin_instance_or_alias):
        if isinstance(plugin_instance_or_alias, str):
            self.alias = plugin_instance_or_alias
        else:
            self.alias = plugin_instance_or_alias.alias

        self.message = "%s is inactive. Some additional software might need to be installed." % (self.alias)

class NoPlugin(UserFeedback):
    pass
