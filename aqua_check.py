# coding=utf-8

import paramiko

def varnish_check(the_host, port, username, password):
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(the_host, port, username, password)
    the_stdin, the_stdout, the_stderr = c.exec_command('/etc/init.d/varnish status')
    the_out, the_err = the_stdout.read(), the_stderr.read()
    if the_err:
        return the_err
    else:
        return the_out

def varnish_run():
    aqua_hosts = ['172.18.10.211', '172.18.10.212']
    username, password = 'root', ''
    status_dict = {}
    for the_host in aqua_hosts:
        status = varnish_check(the_host, 22, username, password)
        status_dict[the_host] = status
    else:
        return status_dict

if __name__ == '__main__':
    status_dict = varnish_run()
    for key, value in status_dict.iteritems():
        print(key)
        print(value)
    print()
    raw_input('End'.center(30, '*'))
