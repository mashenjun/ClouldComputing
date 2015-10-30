__author__ = 'mashenjun'
import os
from boto.s3.connection import S3Connection
from configFile.instanceConfig import Config
from os.path import dirname, join
import cStringIO
from Logger import custome_logger
import SQS.handler as SQS_handler
from dirtools import Dir, DirState
import time
import sys,os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Metrix.timemetrix as mt
# function used to deal with the S3 storage


config = Config()
pirpath = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))
S3_ACCESS_KEY = config.ConfigSectionMap()["aws_access_key_id"]
S3_SECRET_KEY = config.ConfigSectionMap()["aws_secret_access_key"]
REGION_HOST = 's3.eu-central-1.amazonaws.com'
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
LOCAL_IMG = join(pirpath,"images")
LOCAL_RESULT = join(pirpath,"imageResult")
logger = custome_logger.get_logger(__name__)
ERROR_STR = """Error removing %(path)s, %(error)s """
BUCKET_NAME= config.ConfigSectionMap()["s3_bucket_name"]

def connect_to_S3():
    conn_s3 = S3Connection(S3_ACCESS_KEY, S3_SECRET_KEY, host=REGION_HOST)
    # keys = conn_s3.get_all_buckets()
    return conn_s3


def check_bucket(conn_s3):
    if conn_s3.lookup(BUCKET_NAME) is not None:
        return True
    else:
        return False


def create_bucket(conn_s3):
    if check_bucket(conn_s3) is False:
        conn_s3.create_bucket(BUCKET_NAME)


def check_localfolder(folder_name, file_name):
    path = os.path.join(os.path.dirname(__file__), os.path.pardir)
    path_to_file = join(path, folder_name, file_name)
    return os.path.isfile(path_to_file)


def upload_file(conn_s3, name, path_to_result, filename):
    bucket = conn_s3.get_bucket(BUCKET_NAME)
    key = bucket.new_key(join(INPUT_FOLDER, name, filename))
    key.set_contents_from_filename(path_to_result)
    key.set_acl('public-read')

def upload_file_memeory(conn_s3, name, filename, img_array):
    bucket = conn_s3.get_bucket(BUCKET_NAME)
    key = bucket.new_key(join(INPUT_FOLDER, name, filename))
    key.set_contents_from_string(img_array)
    key.set_acl('public-read')



def download_file(conn_s3, name, filename):
    print join(OUTPUT_FOLDER, name, filename)
    key = conn_s3.get_bucket(BUCKET_NAME).get_key(join(OUTPUT_FOLDER, name, filename))
    key.get_contents_to_filename(LOCAL_IMG + '/' + filename)


def send_output_to_s3(conn_s3, name, filename, img_Result):
    img = cStringIO.StringIO()
    img_Result.save(img, 'JPEG')
    bucket = conn_s3.get_bucket(BUCKET_NAME)
    key = bucket.new_key(join(OUTPUT_FOLDER, name, filename))
    key.set_contents_from_string(img.getvalue())


def get_input_from_s3(conn_s3, name, file_name):
    key = conn_s3.get_bucket(BUCKET_NAME).get_key(
        join(INPUT_FOLDER, name, file_name))
    string_result = key.get_contents_as_string()
    logger.info(string_result)
    return string_result


def get_file(conn_s3, name, file_name):
    if check_localfolder("images", file_name) is False:
        key = conn_s3.get_bucket(BUCKET_NAME).get_key(
            join(INPUT_FOLDER, name, file_name))
        key.get_contents_to_filename(LOCAL_IMG + '/' + file_name)
    else:
        logger.info(file_name + "already exists")


def send_file(conn_s3, name):
    path = os.path.join(os.path.dirname(__file__), os.path.pardir)
    path_to_folder = join(path, LOCAL_RESULT)
    FileNames = os.listdir(path_to_folder)
    logger.debug(FileNames[0] + ".=====" + FileNames[1])
    path_to_result1 = join(path_to_folder, FileNames[0])
    path_to_result2 = join(path_to_folder, FileNames[1])
    bucket = conn_s3.get_bucket(BUCKET_NAME)
    key1 = bucket.new_key(join(OUTPUT_FOLDER, name, FileNames[0]))
    key1.set_contents_from_filename(path_to_result1)
    key1.set_acl('public-read')
    key2 = bucket.new_key(join(OUTPUT_FOLDER, name, FileNames[1]))
    key2.set_contents_from_filename(path_to_result2)
    key2.set_acl('public-read')
    
def send_files_head(s3,list_of_files):
    path = os.path.join(os.path.dirname(__file__), os.path.pardir)
    path_to_folder = join(path, LOCAL_IMG)
    bucket = s3.get_bucket(BUCKET_NAME)
    for image in list_of_files:
        time.sleep(0.5)
        mt.startTime_dict[image] = time.clock()
        mt.start_allocate_array.append(time.clock())
        key = bucket.new_key(join(INPUT_FOLDER, image))
        logger.debug(key)
        path_to_result=join(path_to_folder, image)
        logger.debug(path_to_result)
        bytes_sent = 0
        while (bytes_sent == 0):
            bytes_sent = key.set_contents_from_filename(path_to_result)
        key.set_acl('public-read')

def set_dir_for_state():
    path = os.path.join(os.path.dirname(__file__), os.path.pardir)
    path_to_folder = join(path, LOCAL_IMG)
    logger.debug(path_to_folder)
    d = Dir(path_to_folder)
    #can add exclude file hire
    #d = Dir('/path/to/dir', exclude_file='.gitignore')
    #d.is_excluded('/path/to/dir/script.pyc')
    return d
    


def rmgeneric(path, __func__):
    try:
        __func__(path)
        print 'Removed ', path
    except OSError, (errno, strerror):
        print ERROR_STR % {'path': path, 'error': strerror}


def removeall(path):
    if not os.path.isdir(path):
        return
    files = os.listdir(path)
    for x in files:
        fullpath = os.path.join(path, x)
        if os.path.isfile(fullpath):
            f = os.remove
            rmgeneric(fullpath, f)
        elif os.path.isdir(fullpath):
            removeall(fullpath)
            f = os.rmdir
            rmgeneric(fullpath, f)


def clear_local_folder():
    path = os.path.join(os.path.dirname(__file__), os.path.pardir)
    path_to_input = join(path, LOCAL_IMG)
    path_to_output = join(path, LOCAL_RESULT)
    removeall(path_to_input)
    removeall(path_to_output)

def delete_output(conn_s3,name):
    bucket = conn_s3.get_bucket(BUCKET_NAME,validate=False)
    bucketListResultSet = bucket.list(prefix="output/"+name)
    result = bucket.delete_keys([key.name for key in bucketListResultSet])
    return result

def delete_input(conn_s3,name):
    bucket = conn_s3.get_bucket(BUCKET_NAME,validate=False)
    bucketListResultSet = bucket.list(prefix="input/"+name)
    result = bucket.delete_keys([key.name for key in bucketListResultSet])
    return result

def fentch_output(conn_s3,filename):
    bucket = conn_s3.get_bucket(BUCKET_NAME,validate=False)
    bucketListResultSet = bucket.list(prefix="output/"+filename)
    directory = join (LOCAL_RESULT,filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    for item in [key.name for key in bucketListResultSet]:
        name = item.split("/")
        key = conn_s3.get_bucket(BUCKET_NAME).get_key(item)
        key.get_contents_to_filename(join(directory,name[-1]))

    path_to_input = join(LOCAL_IMG,filename)
    removeall(path_to_input)
    