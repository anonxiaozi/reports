# coding=utf-8

import paramiko

def get_scs_jms_msg(the_host, port, username, password):
    command = '/usr/local/mysql/bin/mysql -u *** -p *** -e "select count(*) from jmsdb.jms_messages;" | /usr/bin/tail -1'
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        c.connect(the_host, port, username, password)
    except:
        return 'Defeat'
    jms_stdin, jms_stdout, jms_stderr = c.exec_command(command)
    jms_out, jms_err = jms_stdout.read(), jms_stderr.read()
    if jms_err:
        return jms_err
    else:
        return jms_out

def scs_jms_msg_run():
    host, port, username, password = '172.18.10.52', 22, 'root', ''
    jms_msg = get_scs_jms_msg(host, port, username, password)
    return jms_msg

if __name__ == '__main__':
    result = scs_jms_msg_run()
    print(result)
    print('')
    raw_input('End'.center(30, '*'))
