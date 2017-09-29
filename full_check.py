# coding=utf-8

import os
import xlsxwriter
import datetime

import aqua_check
import db2_jms_check
import disk_check
import multiverse_lsms_check
import scs_jms_check
import service_check
import uml_check

def get_results(cmd):
    the_stdin, the_stdout, the_stderr = os.popen3(cmd)
    the_out, the_err = the_stdout.read(), the_stderr.read()
    if the_err:
        return the_err
    else:
        return the_out

# varnish
aqua_result = aqua_check.varnish_run()

# multiverse & lsms
multiverse_lsms_result = multiverse_lsms_check.lsms_am_run()

# db2_jms
db2_jms_result = db2_jms_check.db2_jms_msg_run()

# scs_jms
scs_jms_result = scs_jms_check.scs_jms_msg_run()

# dwh D space
try:
    dwh_space_result = get_results(r'C:\Python34\python C:\Python27\my_test\pyscripts\xor_check\dwh_space_check.py')
except:
    dwh_space_result = 'None'

# uml array & disk & bwfs
uml_result = uml_check.uml_run()

# disk usage
disk_result = disk_check.disk_space_run()

# service status
service_result = service_check.service_run()

if not os.path.exists(r'C:\Python27\my_test\%s' % str(datetime.datetime.today().strftime('%Y-%m'))):
    os.mkdir(r'C:\Python27\my_test\%s' % str(datetime.datetime.today().strftime('%Y-%m')))

workbook = xlsxwriter.Workbook(r'C:\Python27\my_test\%s\%s_check.xlsx' % (str(datetime.datetime.today().strftime('%Y-%m')), str(datetime.datetime.today().strftime('%Y-%m-%d_%H-%M'))))
red = workbook.add_format({'fg_color': '#ff7575'})
blue = workbook.add_format({'fg_color': '#ACD6FF'})
green = workbook.add_format({'fg_color': 'green'})
top_blue = workbook.add_format({'bold': True, 'font_color': 'blue', 'align': 'top'})
top_red = workbook.add_format({'bold': True, 'font_color': 'red', 'align': 'top'})
font_blue = workbook.add_format({'font_color': 'blue'})
font_red = workbook.add_format({'font_color': 'red'})
bold_blue = workbook.add_format({'bold': True, 'fg_color': '#ACD6FF', 'align': 'center'})
huanhang = workbook.add_format({'text_wrap': True})
bold_blue_left = workbook.add_format({'bold': True, 'fg_color': '#ACD6FF', 'align': 'left'})

# disk_worksheet
disk_check = workbook.add_worksheet('disk')
disk_check.set_column(0, 1, 20)
disk_row, disk_column = 0, 0
sort_disk_host = ['admin1','admin2','aqua1','aqua2','aqua3','lvs1','lvs2','mon','ostr1','ostr2','scs1','scs2','sss1','sss2','wfes1','wfes2','uml1_1','uml1_2','uml2_1','uml2_2']
for disk_host in sort_disk_host:
    disk_info = disk_result[disk_host]
    disk_check.write(disk_row, disk_column, disk_host, bold_blue)
    disk_row += 1
    disk_info = disk_info.split('\n')
    for disk_items in disk_info:
        try:
            disk_path, disk_percent = disk_items.split()[0], disk_items.split()[1]
        except IndexError, e:
            continue
        disk_check.write(disk_row, disk_column, disk_path, huanhang)
        if int(disk_percent.split('%')[0]) > 80:
            disk_check.write(disk_row, disk_column + 1, disk_percent, top_red)
        else:
            disk_check.write(disk_row, disk_column + 1, disk_percent, huanhang)
        disk_row += 1

# uml_worksheet
uml_check = workbook.add_worksheet('uml')
uml_check.set_column(0, 0, 13)
uml_check.set_column(1, 1, 150)
uml_row, uml_column = 0, 0
for the_host, the_info in uml_result.iteritems():
    uml_check.write(uml_row, uml_column, the_host, green)
    uml_row += 1
    for uml_key, uml_value in the_info.iteritems():
        the_value = uml_value.strip('\n').strip().split('\n')
        if not the_value: continue
        if uml_key == 'err':
            uml_check.merge_range(uml_row, uml_column, uml_row + len(the_value), uml_column, uml_key, top_red)
        else:
            uml_check.merge_range(uml_row, uml_column, uml_row + len(the_value), uml_column, uml_key, top_blue)
        for uml_item in the_value:
            uml_check.write(uml_row, uml_column + 1, uml_item, huanhang)
            uml_row += 1
        uml_row += 1

# service_worksheet
service_check = workbook.add_worksheet('services')
service_check.set_column(0, 0, 120)
service_row, service_column = 0, 0
service_host_sort = ['ADMIN1', 'ADMIN2', 'SSS1', 'SSS2', 'SCS1', 'SCS2', 'UML1_1', 'UML1_2', 'UML2_1', 'UML2_2', 'OSTR1', 'OSTR2', 'WFES1', 'WFES2', 'MNT', 'LVS1', 'LVS2']
for service_host in service_host_sort:
    service_info = service_result[service_host]
    service_check.write(service_row, service_column, service_host, bold_blue)
    service_row += 1
#    service_info = service_info.split('\n')
    for service_info_item in service_info:
        service_check.write(service_row, service_column, service_info_item, huanhang)
        service_row += 1
    else:
        service_row += 1

# status_worksheet
status_check = workbook.add_worksheet('status')
status_check.set_column(0, 1, 40)
status_check.merge_range(0, 0, 0, 1, 'Aqua_Varnish_status', bold_blue)
row, column = 0, 0
for aqua_host, varnish_status in aqua_result.items():
    status_check.write(row + 1, column, aqua_host, huanhang)
    status_check.write(row + 1, column + 1, varnish_status.strip('\n'), huanhang)
    row += 1
row += 1
status_check.merge_range(row + 1, column, row + 1, column + 1, 'MULTIVERSE & LSMS status', bold_blue)
row += 1
for the_service, the_status in multiverse_lsms_result.items():
    status_check.write(row + 1, column, the_service.upper(), huanhang)
    if the_status.strip() != 'Running':
        status_check.write(row + 1, column + 1, the_status, red)
    status_check.write(row + 1, column + 1, the_status, huanhang)
    row += 1
row += 1
status_check.write(row + 1, column, 'DB2_JMS_message_count', bold_blue_left)
status_check.write(row + 1, column + 1, str(db2_jms_result).strip('\n'), huanhang)
row += 2
status_check.write(row + 1, column, 'SCS_JMS_message_count', bold_blue_left)
status_check.write(row + 1, column + 1, scs_jms_result.strip('\n'), huanhang)
row += 2
status_check.write(row + 1, column, 'DWH_Space', bold_blue_left)
status_check.write(row + 1, column + 1, dwh_space_result.strip(), huanhang)
row += 2

workbook.close()

