import urllib2 as ulb
from PIL import Image as img
import scipy as sp
from scipy.misc import imread as imgRead
from scipy.signal.signaltools import correlate2d as c2d
import numpy
import io
from flask import flash

class GetImage(object):
    def __init__(self, str_name):
        self.url_input=str_name
    def get_image(self):
        try:
            status=ulb.urlopen(self.url_input)
            if status.getcode()==200:
                fetched_image=ulb.urlopen(self.url_input).read()
                fetched_image=io.BytesIO(fetched_image)
                return fetched_image
        except Exception, e:
            flash("failed:"+str(e))
            return 101

class ScaleImage(object):
    def __init__(self, str_image):
        self.str_image_file=str_image

    def fetch_image(self):
        try:
            image=img.open(self.str_image_file)
            image=image.resize((100, 100), img.ANTIALIAS)
            return image
        except Exception, e:
            flash("failed:"+str(e))
            return 102

class CompareImage(object):
    def get_data(self, str_name):
        try:
            self.image_data=numpy.array(str_name)
            self.image_data=sp.inner(self.image_data, [299, 587, 114])/1000.0
            std_deviation=self.image_data.std()
            if std_deviation==0.0:
                return 103
            return ((self.image_data-self.image_data.mean())/std_deviation)
        except Exception, e:
            flash("failed:"+str(e))
            return 104

    def correlate_image(self, image_one, image_two):
        try:
            max_range=c2d(image_one, image_one, mode='same')
            img_result=c2d(image_one, image_two, mode='same')
            result_final=((img_result.max()/max_range.max())*100)
            return result_final

        except Exception, e:
            flash("failed:"+str(e))
            return 105

def main(p1, p2):
    img_one=GetImage(p1)
    fetched_img_one=img_one.get_image()
    if fetched_img_one==101:
        return 101
    img_two=GetImage(p2)
    fetched_img_two=img_two.get_image()
    if fetched_img_two==101:
        return 101
    img_one=ScaleImage(fetched_img_one)
    pic1=img_one.fetch_image()
    if pic1==102:
        return 102
    img_two=ScaleImage(fetched_img_two)
    pic2=img_two.fetch_image()
    if pic2==102:
        return 102
    imge=CompareImage()
    image1=imge.get_data(pic1)
    image2=imge.get_data(pic2)
    meg=imge.correlate_image(image1, image2)
    return meg
