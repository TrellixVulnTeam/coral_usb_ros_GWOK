#!/usr/bin/env python

import os
import tarfile

import rospkg

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve


url = 'https://dl.google.com/coral/canned_models/all_models.tar.gz'
seg_urls = [
    'https://github.com/google-coral/edgetpu/raw/master/test_data/'
    'deeplabv3_mnv2_dm05_pascal_quant_edgetpu.tflite',
    'https://github.com/google-coral/edgetpu/raw/master/test_data/'
    'deeplabv3_mnv2_pascal_quant_edgetpu.tflite',
]


rospack = rospkg.RosPack()
pkg_path = rospack.get_path('coral_usb')
models_path = os.path.join(pkg_path, './models')
tar_path = os.path.join(models_path, 'all_models.tar.gz')
if not os.path.exists(models_path):
    os.makedirs(models_path)
urlretrieve(url, tar_path)

with tarfile.open(tar_path) as tar_f:
    def is_within_directory(directory, target):
        
        abs_directory = os.path.abspath(directory)
        abs_target = os.path.abspath(target)
    
        prefix = os.path.commonprefix([abs_directory, abs_target])
        
        return prefix == abs_directory
    
    def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
    
        for member in tar.getmembers():
            member_path = os.path.join(path, member.name)
            if not is_within_directory(path, member_path):
                raise Exception("Attempted Path Traversal in Tar File")
    
        tar.extractall(path, members, numeric_owner=numeric_owner) 
        
    
    safe_extract(tar_f, models_path)

for seg_url in seg_urls:
    filename = seg_url.split('/')[-1]
    filepath = os.path.join(models_path, filename)
    urlretrieve(seg_url, filepath)
