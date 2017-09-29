# coding=utf-8

# python 3

import shutil

def get_dwh_space(path='d:'):
    space = shutil.disk_usage(path)
    free = '%0.2f' % (space.free / 1024 / 1024)
    return '%s MB' % free

if __name__ == '__main__':
    result = get_dwh_space()
    print(result)
