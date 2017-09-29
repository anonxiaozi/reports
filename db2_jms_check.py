# coding=utf-8

# python 3

import pymssql

def get_db2_jms_msg(host,user,password,database):
    c = pymssql.connect(host, user, password, database)
    cur = c.cursor()
    cur.execute("select COUNT(*) from JMS_MESSAGES")
    fetch = cur.fetchone()
    cur.close()
    c.close()
    return fetch

def db2_jms_msg_run():
    output = get_db2_jms_msg('172.18.10.71','','','')
    if output:
        return output[0]
    else:
        return 0

if __name__ == '__main__':
    count = db2_jms_msg_run()
    print(count)
