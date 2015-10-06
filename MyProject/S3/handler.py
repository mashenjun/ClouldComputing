__author__ = 'mashenjun'
import boto
import os
from boto.s3.connection import S3Connection
from configFile.instanceConfig import Config
from os.path import dirname, join
# function used to deal with the S3 storage
config = Config()

S3_ACCESS_KEY = config.ConfigSectionMap()["aws_access_key_id"]
S3_SECRET_KEY = config.ConfigSectionMap()["aws_secret_access_key"]
REGION_HOST = 's3.eu-central-1.amazonaws.com'
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

def connect_to_S3():
    conn_s3 = S3Connection(S3_ACCESS_KEY, S3_SECRET_KEY, host = REGION_HOST)
    # keys = conn_s3.get_all_buckets()
    return conn_s3


def check_bucket(conn_s3):
    if conn_s3.lookup(config.ConfigSectionMap()["s3_bucket_name"]) is not True:
        return True
    else:
        return False

def create_bucket(conn_s3):
    if check_bucket(conn_s3) is False:
        conn_s3.create_bucket(config.ConfigSectionMap()["s3_bucket_name"])


def upload_file(conn_s3,name,filename):
    bucket = conn_s3.get_bucket(config.ConfigSectionMap()["s3_bucket_name"]);
    key = bucket.new_key(join(INPUT_FOLDER,name,filename))
    key.set_contents_from_filename('PATH/TO/FILE')
    key.set_acl('public-read')

def download_file(conn_s3,name, filename):
    key = conn_s3.get_bucket(config.ConfigSectionMap()["s3_bucket_name"]).get_key(join(OUTPUT_FOLDER,name,filename))
    key.get_contents_to_filename('/'+filename)

def output_to_s3():