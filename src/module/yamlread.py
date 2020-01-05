import yaml

def read_yaml_setting_value(file_name: object) -> object:
    f = open(file_name, encoding='UTF8')
    # use safe_load instead load
    data = yaml.safe_load(f)
    f.close()
    return data


