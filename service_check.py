# coding=utf-8

import paramiko

def service_check(the_host, username, password, services):
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    commands = ['cd']
    for service in services:
        commands.append('/etc/init.d/%s status' % service)
    cmd = ' ; '.join(commands)
    try:
        c.connect(the_host, 22, username, password)
    except TimeoutError as e:
        return e
    the_stdin, the_stdout, the_stderr = c.exec_command(cmd)
    the_out, the_err = the_stdout.read(), the_stderr.read()
    c.close()
    return the_out, the_err

def ha_check(the_host, username, password, commands):
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        c.connect(the_host, 22, username, password)
    except TimeoutError as e:
        return e
    the_stdin, the_stdout, the_stderr = c.exec_command(commands)
    the_out, the_err = the_stdout.read(), the_stderr.read()
    c.close()
    return the_out, the_err

def service_run():
    results = {}
    ha_host_dict = {
        'ADMIN1' : ['172.18.10.60', 'root', '', '/usr/sbin/pcs status'],
        'ADMIN2' : ['172.18.10.62', 'root', '', '/usr/sbin/pcs status'],
        'SSS1'   : ['172.18.10.120', 'root', '', '/usr/sbin/pcs status'],
        'SSS2'   : ['172.18.10.122', 'root', '', '/usr/sbin/pcs status'],
        'SCS1'   : ['172.18.10.52', 'root', '', '/usr/sbin/pcs status'],
        'SCS2'   : ['172.18.10.54', 'root', '', '/usr/sbin/pcs status'],
        'UML1_1' : ['172.18.10.40', 'root', '', '/usr/sbin/crm_mon -1'],
        'UML1_2' : ['172.18.10.42', 'root', '', '/usr/sbin/crm_mon -1'],
        'UML2_1' : ['172.18.10.44', 'root', '', '/usr/sbin/crm_mon -1'],
        'UML2_2' : ['172.18.10.46', 'root', '', '/usr/sbin/crm_mon -1'],
        'OSTR1'  : ['172.18.10.124', 'root', '', '/usr/sbin/pcs status'],
        'OSTR2'  : ['172.18.10.126', 'root', '', '/usr/sbin/pcs status'],
    }
    host_dict = {
        'WFES1'  : ['172.18.10.101', 'root', '', ['wfes', 'sentry']],
        'WFES2'  : ['172.18.10.102', 'root', '', ['wfes', 'sentry']],
        'MNT'    : ['172.18.10.201', 'root', '', ['monitorcenter', 'mysql']],
        'LVS1'   : ['172.18.10.221', 'root', '', ['keepalived']],
        'LVS2'   : ['172.18.10.222', 'root', '', ['keepalived']],
    }
    for ha_host, ha_info in ha_host_dict.iteritems():
        the_host, username, password, commands = ha_info
        results[ha_host] = ha_check(the_host, username, password, commands)
    else:
        for host, service_info in host_dict.iteritems():
            the_host, username, password, commands = service_info
            results[host] = service_check(the_host, username, password, commands)
    return results

if __name__ == '__main__':
    results = service_run()
    for key, value in results.iteritems():
        print(key)
        print(value)
    print()
    raw_input('End'.center(30, '*'))
