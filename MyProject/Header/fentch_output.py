__author__ = 'mashenjun'
import sys,os.path
from configFile.instanceConfig import Config
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import S3.handler as s3h

config = Config()
BUCKET_NAME= config.ConfigSectionMap()["s3_bucket_name"]


def fentch(name):
    s3 = s3h.connect_to_S3()
    bucket = s3.get_bucket(BUCKET_NAME,validate=False)
    bucketListResultSet = bucket.list(prefix="output/"+name)
    for item in [key.name for key in bucketListResultSet]:
        key = s3h.get_bucket(BUCKET_NAME).get_key(item)
        key.get_contents_to_filename(LOCAL_IMG + '/' + filename)

