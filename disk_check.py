# coding=utf-8

import paramiko

def get_disk_space(the_host, port, username, password):
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        c.connect(the_host, 22, username, password)
    except:
        return('%s:%s connect failed.' % (the_host, port))
    disk_stdin, disk_stdout, disk_stderr = c.exec_command("df -PHT | sed '1d' | awk '{print $7,$6}'")
    data = ''.join(disk_stdout.readlines())
    return(data)

def disk_space_run():
    sort_key = ['admin1','admin2','aqua1','aqua2','aqua3','lvs1','lvs2','mon','ostr1','ostr2','scs1','scs2','sss1','sss2','wfes1','wfes2','uml1_1','uml1_2','uml2_1','uml2_2']
    host_dict = {
        'admin1': ['172.18.10.60'],
        'admin2': ['172.18.10.62'],
        'aqua1' : ['172.18.10.210'],
        'aqua2' : ['172.18.10.211'],
        'aqua3' : ['172.18.10.212'],
        'lvs1'  : ['172.18.10.221'],
        'lvs2'  : ['172.18.10.222'],
        'mon'   : ['172.18.10.201'],
        'ostr1' : ['172.18.10.124'],
        'ostr2' : ['172.18.10.126'],
        'scs1'  : ['172.18.10.52'],
        'scs2'  : ['172.18.10.54'],
        'sss1'  : ['172.18.10.120'],
        'sss2'  : ['172.18.10.122'],
        'wfes1' : ['172.18.10.101'],
        'wfes2' : ['172.18.10.102'],
        'uml1_1': ['172.18.10.40', ''],
        'uml1_2': ['172.18.10.42', ''],
        'uml2_1': ['172.18.10.44', ''],
        'uml2_2': ['172.18.10.46', ''],
    }
    result_dict = {}
    for the_host in sort_key:
        if len(host_dict[the_host]) > 1:
            password = host_dict[the_host][1]
        else:
            password = ''
        result_dict[the_host] = (get_disk_space(host_dict[the_host][0], 22, 'root', password))
    else:
        return result_dict

if __name__ == '__main__':
    result = disk_space_run()
    for the_host, the_info in result.iteritems():
        print(the_host)
        print(the_info)
    print('')
    raw_input('End'.center(30, '*'))