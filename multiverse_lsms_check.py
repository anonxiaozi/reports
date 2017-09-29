# coding=utf-8

import urllib
import urllib2
import sys

def check_lsms_am(url, sign):
    try:
        data = urllib2.urlopen(url, timeout=5)
    except urllib2.URLError as e:
        return False
    if sign in data.read():
        return True

def lsms_am_run():
    output = {}
    lsms_am_url = {
        'lsms': 'http://172.18.10.62:7070/lsms/main.htm',
        'multiverse': 'http://172.18.10.60:8080/am/framework.htm',
    }
    lsms_am_sign = {
        'lsms': '<title>Local Subscriber Management System</title>',
        'multiverse': '<TITLE>AM</TITLE>'
    }

    for key, value in lsms_am_url.iteritems():
        if check_lsms_am(value, lsms_am_sign[key]):
            output[key] = 'Running'
        else:
            output[key] = 'Stopped'
    else:
        return(output)

if __name__ == '__main__':
    status = lsms_am_run()
    print(status)
    print('')
    raw_input('End'.center(30, '*'))