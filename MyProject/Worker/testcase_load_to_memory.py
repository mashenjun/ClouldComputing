__author__ = 'mashenjun'
import sys,os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from imageHandler import read_image_to_string
from S3 import handler as S3_handler

conn_s3 = S3_handler.connect_to_S3()

im_string= read_image_to_string("china.jpg")
S3_handler.upload_file_memeory(conn_s3,"",'china.txt',im_string)


