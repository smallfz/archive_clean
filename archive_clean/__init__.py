#-*- coding: utf-8 -*-

import os, sys, shutil, time, datetime, re


class Cleaner(object):
    '''
    example:

    # cleaner = Cleaner()
    # cleaner.add_dir(r'/home/user/pg_dumps', 
    #                 keep_hours=48, 
    #                 min_keep_count=2, 
    #                 pattern=r'\.sql$')
    # cleaner.process()

    '''

    def __init__(self):
        self.dirs = []

    def add_dir(self, _dir,
                keep_hours=168,
                min_keep_count=7,
                pattern=None):
        '''add_dir(dir, 
                   keep_hours=168, 
                   min_keep_count=7, 
                   pattern=None|regexp_str)
        '''
        _dir = os.path.abspath(_dir)
        if os.path.isdir(_dir):
            self.dirs.append((_dir, keep_hours, min_keep_count, pattern))

    def process(self):
        '''do cleanning. (before call this, add some dirs.)'''
        if not self.dirs:
            print 'no dirs.'
            return
        for _dir, keep_hours, min_keep_count, pt in self.dirs:
            self._process_dir(_dir, keep_hours, min_keep_count, pt)

    def _process_dir(self, _dir, keep_hours, min_keep_count, pt):
        if pt and isinstance(pt, (str, unicode)):
            names = [n for n in os.listdir(_dir) \
                     if re.search(pt, n, re.I|re.S)]
        else:
            names = [n for n in os.listdir(_dir)]
        if not names:
            return
        files = []
        for name in names:
            path = os.path.join(_dir, name)
            if os.path.isfile(path):
                st = os.stat(path)
                files.append((path, st.st_ctime))
        files = sorted(files, key=lambda row: row[1], reverse=True)
        # for row in files:
        #     print row[0], row[1]
        if len(files) < min_keep_count and min_keep_count > 0:
            return
        if min_keep_count <= 0:
            min_keep_count = 0
        files = reversed(files[min_keep_count:])
        HOUR, now = 3600, time.time()
        for row in files:
            if row[1] + HOUR * keep_hours < now:
                os.unlink(row[0])
                print os.path.basename(row[0]), 'removed.'

    
if __name__ == '__main__':
    print Cleaner.__doc__
    # c = Cleaner()
    # c.add_dir(r'D:\xl-photos\1701210012119',
    #           keep_hours=48,
    #           min_keep_count=2,
    #           pattern=r'\.jpg$')
    # c.process()
