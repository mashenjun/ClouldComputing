

__author__ = 'mashenjun'
from scipy.misc import imread,imsave
import os,cPickle
from os.path import dirname, join


IMAGE_FOLDER = "images"
IMAGE_RESULT_FOLDER = "imageResult"
MODULE_PATH = dirname(os.path.abspath(__file__))
def read_image(imagename):
    #module_path = dirname(os.path.abspath(__file__))
    filename = join(MODULE_PATH,IMAGE_FOLDER,imagename)
    image = imread(filename)
    return image

def save_image(array,filename):
    #module_path = dirname(os.path.abspath(__file__))
    filepath = join(MODULE_PATH,IMAGE_RESULT_FOLDER,filename)
    imsave(filepath,array)

def delet_result():
    folder = join(MODULE_PATH,IMAGE_RESULT_FOLDER)
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception, e:
            print e

def read_image_to_string(imagename):
    img = read_image(imagename)
    im_string = cPickle.dumps(img)
    return im_string
# def main():
#     readimage("china.jpg")
#
# if __name__ == "__main__":
#     main()
