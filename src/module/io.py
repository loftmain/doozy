import os
import platform

def get_refined_path(path):
    if platform.system() == 'Windows':
        refined_path = path.split('file:///')[1]
    elif platform.system() == 'Linux':
        refined_path = path.split('file://')[1]
    return refined_path


def set_save_folder(path, opt):
    if not os.path.exists(os.path.join(path, 'save')):
        os.mkdir(os.path.join(path, 'save'))
    save_path = os.path.join(path, 'save')
    if opt == 'marking':
        if not os.path.exists(os.path.join(save_path, 'marking')):
            os.mkdir(os.path.join(save_path, 'marking'))
        save_path = os.path.join(save_path, 'marking')
    elif opt == 'backtesting':
        if not os.path.exists(os.path.join(save_path, 'backtesting')):
            os.mkdir(os.path.join(save_path, 'backtesting'))
        save_path = os.path.join(save_path, 'backtesting')
    elif opt == 'modeling':
        if not os.path.exists(os.path.join(save_path, 'modeling')):
            os.mkdir(os.path.join(save_path, 'modeling'))
        save_path = os.path.join(save_path, 'modeling')
    elif opt == 'order':
        if not os.path.exists(os.path.join(save_path, 'order')):
            os.mkdir(os.path.join(save_path, 'order'))
        save_path = os.path.join(save_path, 'order')
    return save_path
