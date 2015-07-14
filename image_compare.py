import urllib2 as ulb
from PIL import Image as img
import scipy as sp
from scipy.misc import imread as imgRead
from scipy.signal.signaltools import correlate2d as c2d
import numpy
import io



class GetImage(object):
    def get_image(self):
        while True:
            try:
                self.url_input=raw_input("Enter the url:")
                if self.is_not_an_image( ):
                    print "\nNot a link to an Image\n"
                    continue
                request_url = ulb.Request(self.url_input, headers={'User-Agent' : "Magic Browser"})
                print "\nFetching Image\n"
                status=ulb.urlopen(request_url)
                if status.getcode()==200:
                    image_data=status.read()
                    image_data=io.BytesIO(image_data)
                    self.image_file=image_data;
                else:
                    print "\nurl error! File not found at url!\n"
                    continue
                break
            except:
                print "\nAn error ocured. Please retry!\n"

    def scale_image(self):
        try:
            image=img.open(self.image_file)
            is_notjpg=self.is_ext_notjpg()
            if is_notjpg:
                image=self.convert_to_jpg(image)
            image=image.resize((100, 100), img.ANTIALIAS)
            return image
        except:
            print "\nImage data corrupted! please retry!\n"
            exit()

    def is_ext_notjpg(self):
        if self.url_input.endswith(('.png', '.gif', '.tiff', '.bmp', '.gif')):
            return True
        return False

    def is_not_an_image(self):
        if self.url_input.endswith(('.png', '.gif', '.tiff', '.bmp', '.gif', '.jpg')):
            return False
        return True

    def convert_to_jpg(self, old_image):
        new_image = img.new("RGB", old_image.size, (255,255,255))
        new_image.paste(old_image,(0,0), old_image)
        new_image.save("temp.jpg", "JPEG")
        new_image = img.open("temp.jpg")
        return new_image

class CompareImage(object):
    def __init__(self):
        print "\ncomparing images\n"

    def get_data(self, str_name):
        try:
            self.image_data=numpy.array(str_name)
            self.image_data=sp.inner(self.image_data, [299, 587, 114])/1000.0
            std_deviation=self.image_data.std()
            if std_deviation==0.0:
                print "\nImage error! Please retry!\n"
                exit()
            return ((self.image_data-self.image_data.mean())/std_deviation)
        except:
            print "\nAwwh, somethings not right! Try again\n"
            exit()

    def correlate_image(self, image_one, image_two):
        try:
            max_range=c2d(image_one, image_one, mode='same')
            img_result=c2d(image_one, image_two, mode='same')
            result_final=((img_result.max()/max_range.max())*100)
            print "Images are", result_final,"percent similar\n"
            if result_final==100.0:
                print"Images are exactly same\n"
            elif result_final==0.0:
                print "Images are very different\n"
        except:
            print "\nAwwh, somethings not right! Try again\n"
            exit()

def main():
    img_one=GetImage()
    img_one.get_image()
    pic1=img_one.scale_image()
    img_two=GetImage()
    img_two.get_image()
    pic2=img_two.scale_image()
    imge=CompareImage()
    image1=imge.get_data(pic1)
    image2=imge.get_data(pic2)
    imge.correlate_image(image1, image2)

if __name__ == "__main__":
    main()
