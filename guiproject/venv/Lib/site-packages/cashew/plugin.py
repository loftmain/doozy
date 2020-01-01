from cashew.exceptions import InactivePlugin
from cashew.exceptions import InternalCashewException
from cashew.exceptions import NoPlugin
from cashew.exceptions import UserFeedback
import inflection
import inspect
import os
import sys
import yaml

class Plugin(object):
    """
    Base class for plugins. Define instance methods shared by plugins here.
    """
    aliases = []
    _class_settings = { "max-docstring-length" : None }
    _settings = {
            "install-dir" : ("Location where the plugin was defined.", None)
            }

    def is_active(self):
        return True

    def standard_alias(self):
        return self.setting('aliases')[0]

    def name(self):
        return inflection.titleize(self.standard_alias())

    def initialize_settings(self, **raw_kwargs):
        self._instance_settings = {}

        self.initialize_settings_from_parents()
        self.initialize_settings_from_other_classes()
        self.initialize_settings_from_raw_kwargs(raw_kwargs)

    def initialize_settings_from_parents(self):
        for parent_class in self.__class__.imro():
            if parent_class._settings:
                self.update_settings(parent_class._settings)
            if hasattr(parent_class, '_unset'):
                for unset in parent_class._unset:
                    del self._instance_settings[unset]
    
    def initialize_settings_from_other_classes(self):
        if hasattr(self.__class__, 'aliases') and self.__class__.aliases:
            for parent_class in self.__class__.imro():
                for alias in parent_class.aliases:
                    settings_from_other_classes = PluginMeta._store_other_class_settings.get(alias)
                    if settings_from_other_classes:
                        self.update_settings(settings_from_other_classes)

    def initialize_settings_from_raw_kwargs(self, raw_kwargs):
        hyphen_settings = dict(
                (k, v)
                for k, v in raw_kwargs.items()
                if k in self._instance_settings)

        underscore_settings = dict(
                (k.replace("_", "-"), v)
                for k, v in raw_kwargs.items()
                if k.replace("_", "-") in self._instance_settings)

        self.update_settings(hyphen_settings)
        self.update_settings(underscore_settings)

    def safe_setting(self, name_hyphen, default=None):
        """
        Retrieves the setting value, but returns a default value rather than
        raising an error if the setting does not exist.
        """
        try:
            return self.setting(name_hyphen)
        except UserFeedback:
            return default

    def setting(self, name_hyphen):
        """
        Retrieves the setting value whose name is indicated by name_hyphen.

        Values starting with $ are assumed to reference environment variables,
        and the value stored in environment variables is retrieved. It's an
        error if thes corresponding environment variable it not set.
        """
        if name_hyphen in self._instance_settings:
            value = self._instance_settings[name_hyphen][1]
        else:
            msg = "No setting named '%s'" % name_hyphen
            raise UserFeedback(msg)

        if isinstance(value, str) and value.startswith("$"):
            env_var = value.lstrip("$")
            if env_var in os.environ:
                return os.getenv(env_var)
            else:
                msg = "'%s' is not defined in your environment" % env_var
                raise UserFeedback(msg)

        elif isinstance(value, str) and value.startswith("\$"):
            return value.replace("\$", "$")

        else:
            return value

    def setting_values(self, skip=None):
        """
        Returns dict of all setting values (removes the helpstrings).
        """
        if not skip:
            skip = []

        return dict(
                (k, v[1])
                for k, v in self._instance_settings.items()
                if not k in skip)

    def update_settings(self, new_settings):
        """
        Update settings for this instance based on the provided dictionary of
        setting keys: setting values. Values should be a tuple of (helpstring,
        value,) unless the setting has already been defined in a parent class,
        in which case just pass the desired value.
        """
        self._update_settings(new_settings, False)

    def _update_settings(self, new_settings, enforce_helpstring=True):
        """
        This method does the work of updating settings. Can be passed with
        enforce_helpstring = False which you may want if allowing end users to
        add arbitrary metadata via the settings system.

        Preferable to use update_settings (without leading _) in code to do the
        right thing and always have docstrings.
        """
        for raw_setting_name, value in new_settings.items():
            setting_name = raw_setting_name.replace("_", "-")

            setting_already_exists = setting_name in self._instance_settings
            value_is_list_len_2 = isinstance(value, list) and len(value) == 2
            treat_as_tuple = not setting_already_exists and value_is_list_len_2

            if isinstance(value, tuple) or treat_as_tuple:
                self._instance_settings[setting_name] = value

            else:
                if setting_name not in self._instance_settings:
                    if enforce_helpstring:
                        msg = "You must specify param '%s' as a tuple of (helpstring, value)"
                        raise InternalCashewException(msg % setting_name)

                    else:
                        # Create entry with blank helpstring.
                        self._instance_settings[setting_name] = ('', value,)

                else:
                    # Save inherited helpstring, replace default value.
                    orig = self._instance_settings[setting_name]
                    self._instance_settings[setting_name] = (orig[0], value,)

    def settings_and_attributes(self):
        """Return a combined dictionary of setting values and attribute values."""
        attrs = self.setting_values()
        attrs.update(self.__dict__)
        skip = ["_instance_settings", "aliases"]
        for a in skip:
            del attrs[a]
        return attrs

class PluginMeta(type):
    """
    Base meta class for anything plugin-able.
    """
    _store_other_class_settings = {} # allow plugins to define settings for other classes

    def __lt__(cls, other):
        return cls.__name__ < other.__name__

    def __init__(cls, name, bases, attrs):
        assert issubclass(cls, Plugin), "%s should inherit from class Plugin" % name

        if not hasattr(cls, 'plugins'):
            cls.plugins = {}

        if hasattr(cls, 'aliases'):
            cls.register_plugin(cls.aliases, cls, {})

        cls.register_other_class_settings()

    def register_other_class_settings(cls):
        if hasattr(cls, '_other_class_settings') and cls._other_class_settings:
            for other_class_key, other_class_settings in cls._other_class_settings.items():
                if other_class_key not in PluginMeta._store_other_class_settings:
                    PluginMeta._store_other_class_settings[other_class_key] = {}

                PluginMeta._store_other_class_settings[other_class_key].update(other_class_settings)

    def register_plugin(cls, alias_or_aliases, class_or_class_name, settings):
        aliases = cls.standardize_alias_or_aliases(alias_or_aliases)
        klass = cls.get_reference_to_class(class_or_class_name)

        # Ensure 'aliases' and 'help' settings are set.
        settings['aliases'] = ('aliases', aliases)
        if 'help' not in settings:
            docstring = klass.check_docstring()
            settings['help'] = ("Helpstring for plugin.", docstring)

        # Create the tuple which will be registered for the plugin.
        class_info = (class_or_class_name, settings)

        # Register the class_info tuple for each alias.
        for alias in aliases:
            if isinstance(class_or_class_name, type):
                modname = class_or_class_name.__module__
                alias = cls.apply_prefix(modname, alias)

            cls.plugins[alias] = class_info

    def standardize_alias_or_aliases(cls, alias_or_aliases):
        """
        Make sure we don't attempt to iterate over an alias string thinking
        it's an array.
        """
        if isinstance(alias_or_aliases, str):
            return [alias_or_aliases]
        else:
            return alias_or_aliases

    def get_reference_to_class(cls, class_or_class_name):
        """
        Detect if we get a class or a name, convert a name to a class.
        """
        if isinstance(class_or_class_name, type):
            return class_or_class_name

        elif isinstance(class_or_class_name, str):
            if ":" in class_or_class_name:
                mod_name, class_name = class_or_class_name.split(":")

                if not mod_name in sys.modules:
                    __import__(mod_name)

                mod = sys.modules[mod_name]
                return mod.__dict__[class_name]

            else:
                return cls.load_class_from_locals(class_or_class_name)

        else:
            msg = "Unexpected Type '%s'" % type(class_or_class_name)
            raise InternalCashewException(msg)

    def load_class_from_locals(cls, class_name):
        raise Exception("not implemented")

    def check_docstring(cls):
        """
        Asserts that the class has a docstring, returning it if successful.
        """
        docstring = inspect.getdoc(cls)
        if not docstring:
            breadcrumbs = " -> ".join(t.__name__ for t in inspect.getmro(cls)[:-1][::-1])
            msg = "docstring required for plugin '%s' (%s, defined in %s)"
            args = (cls.__name__, breadcrumbs, cls.__module__)
            raise InternalCashewException(msg % args)

        max_line_length = cls._class_settings.get('max-docstring-length')
        if max_line_length:
            for i, line in enumerate(docstring.splitlines()):
                if len(line) > max_line_length:
                    msg = "docstring line %s of %s is %s chars too long" 
                    args = (i, cls.__name__, len(line) - max_line_length)
                    raise Exception(msg % args)

        return docstring

    def apply_prefix(cls, modname, alias):
        return alias

    def register_plugins(cls, plugin_info):
        for k, v in plugin_info.items():
            cls.register_plugin(k.split("|"), v[0], v[1])

    def register_plugins_from_dict(cls, yaml_content, install_dir=None):
        for alias, info_dict in yaml_content.items():
            if ":" in alias:
                _, alias = alias.split(":")

            if 'class' in info_dict:
                class_name = info_dict['class']
                del info_dict['class']
            else:
                class_name = cls.__name__

            info_dict['aliases'] = [alias]
            info_dict['install-dir'] = install_dir
            cls.register_plugin(alias.split("|"), class_name, info_dict)

    def register_plugins_from_yaml_file(cls, yaml_file):
        with open(yaml_file, 'rb') as f:
            yaml_content = yaml.safe_load(f.read())

        install_dir = os.path.dirname(yaml_file)
        cls.register_plugins_from_dict(yaml_content, install_dir)

    def create_instance(cls, alias, *instanceargs, **instancekwargs):
        alias = cls.adjust_alias(alias)

        if not alias in cls.plugins:
            msg = "no alias '%s' available for '%s'"
            msgargs = (alias, cls.__name__)
            raise NoPlugin(msg % msgargs)

        class_or_class_name, settings = cls.plugins[alias]
        klass = cls.get_reference_to_class(class_or_class_name)

        instance = klass(*instanceargs, **instancekwargs)
        instance.alias = alias

        if not hasattr(instance, '_instance_settings'):
            instance.initialize_settings()
        instance.update_settings(settings)

        if not instance.is_active():
            raise InactivePlugin(alias)

        return instance

    def adjust_alias(cls, alias):
        return alias

    def imro(cls):
        """
        Returns MRO in reverse order, skipping 'object/type' class.
        """
        return reversed(inspect.getmro(cls)[0:-2])

    def __iter__(cls, *instanceargs):
        """
        Lets you iterate over instances of all plugins which are not marked as
        'inactive'. If there are multiple aliases, the resulting plugin is only
        called once.
        """
        processed_aliases = set()

        for alias in sorted(cls.plugins, key=str.lower):
            if alias in processed_aliases:
                # duplicate alias
                continue

            try:
                instance = cls.create_instance(alias, *instanceargs)
                instance.alias = instance.standard_alias()
                yield(instance)
                for alias in instance.setting('aliases'):
                    processed_aliases.add(alias)

            except InactivePlugin:
                pass
