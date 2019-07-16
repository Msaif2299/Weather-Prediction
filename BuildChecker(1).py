import os
cur_dir = os.getcwd()
if not os.path.exists('data'):
    os.mkdir(cur_dir + r'/data/')
