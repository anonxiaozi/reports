# coding=utf-8

import os
import re
import sys
import time

class GETVIDEO(object):

    """
    下载视频文件
    get_video_list用来获取节目ID,然后将节目名称和video_name_prefix合并,
        最后生成字典:key为节目名,value为节目ID
    _exec方法,通过循环节目字典,执行下载命令
    _exit 方法，用来抛出异常时调用,直接使用os._exit退出
    """
    
    video_dict = {}
    id_dict = {}
    path_dict = {}
    
    def __init__(self, video_file, video_name_prefix, dest_dir, speed_re):
        self.video_file = video_file
        self.video_name_prefix = video_name_prefix
        self.dest_dir = dest_dir
        self.speed_re = speed_re
        self.video_num = 40
        self.video_dict = {}
    
    def get_video_list(self):
        """获取节目ID、名称,生成节目字典"""
        with open(video_file, 'rb') as f:
            for line in f.xreadlines():
                pid = line.strip()
                self.video_num += 1
                video_name = self.video_name_prefix + '_' + str(self.video_num)
                self.video_dict[video_name] = pid
    
    def _exec(self):
        """执行下载任务"""
        for key, value in self.video_dict.iteritems():
            raw_data = os.popen('scp dump asset %s' % value).read()
            try:
                speed_id = self.speed_re.findall(raw_data)[0]
            except Exception as e:
                print(key)
                print(e)
                continue
            final_id = value + '.' + speed_id
            print 'scp export \httpdevices\\%s %s' % (final_id, os.path.join(self.dest_dir, key))
            os.system('scp export \httpdevices\\%s %s' % (final_id, os.path.join(self.dest_dir, key)))

    @staticmethod
    def _exit(data=''):
        """退出脚本"""
        print('Exit: %s' % data)
        os._exit(1)
    
    def __del__(self):
        print('Download completed.'.center(50, '*'))


if __name__ == '__main__':
    os.chdir(u'c:\\vstrmkit')
    dest_dir, video_file, video_name_prefix = 'C:\\video_test\\guojixinwen', 'c:\\video_test\\guojixinwen.txt', ''
    speed_re = re.compile('Sub-file\s0\s+\(\S+\s?\S+\s?\S+\s?\)\:\n\s+File\sExtension\s+(\S+)', re.S)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    if not os.path.exists(video_file):
        GETVIDEO._exit('File not found: [%s]' % video_file)
    get_video = GETVIDEO(video_file, video_name_prefix, dest_dir, speed_re)
    get_video.get_video_list()
    get_video._exec()


