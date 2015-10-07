__author__ = 'mashenjun'
import imageProcess
from S3 import handler

conn_s3 = handler.connect_to_S3()
handler.get_file(conn_s3,'','china.jpg')
imageProcess.process_image('china.jpg')
handler.send_file(conn_s3,'')
