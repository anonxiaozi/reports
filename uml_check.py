# coding=utf-8

import paramiko

def get_uml_array(the_host, username, password):
    the_array_info = []
    the_array_err = ''
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        c.connect(the_host, 22, username, password)
    except:
        return '%s connect faild.' % the_host
    array_stdin, array_stdout, array_stderr = c.exec_command('bcadm -M -qa')
    disk_stdin, disk_stdout, disk_stderr = c.exec_command("df -PHT | sed '1d' | awk '{print $7,$6}'")
    bwfs_stdin, bwfs_stdout, bwfs_stderr = c.exec_command("bwadmin -l")
    bwfs_status = '\n'.join(bwfs_stdout.readlines())
    the_disk_info = '\n'.join(disk_stdout.readlines())
    for line in array_stdout.readlines()[-10:]:
        the_array_info.append(line)
    array_err = array_stderr.read()
    if array_err:
        the_array_err = array_err
    c.close()
    return '\n'.join(the_array_info), the_array_err, the_disk_info, bwfs_status

def uml_run():
    uml_hosts = ['172.18.10.40', '172.18.10.42', '172.18.10.44', '172.18.10.46']
    username = 'root'
    password = ''
    array_info = {}
    for the_host in uml_hosts:
        array_info[the_host] = {}
        the_array_info, the_array_err, the_disk_info, bwfs_info = get_uml_array(the_host, username, password)
        array_info[the_host]['info'] = the_array_info
        if the_array_err:
            array_info[the_host]['err'] = the_array_err
        else:
            array_info[the_host]['err'] = ''
        array_info[the_host]['diskspace'] = the_disk_info
        array_info[the_host]['bwfs'] = bwfs_info
    return array_info

if __name__ == '__main__':
    array_info = uml_run()
    for key, value in array_info.iteritems():
        print(key)
        print(value)
    print()
    raw_input('End'.center(30, '*'))
