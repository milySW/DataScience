from google_images_download import google_images_download 
import os

default_fast_food = "fast food, hamburger, kebab, pizza, french fries, chicken popeyes, burito, unhealthy food, unhealthy diet, fatty food, hot dog"
default_slow_food = "healthy meal, vegetables, fruit, fit meal, walnuts dinner, fish dinner, green beans dinner, healthy diet, salad, diet food"

def my_scraper(keywords_1=default_fast_food, keywords_2=default_slow_food):
    """
    Function downloading images from google gallery.
    :param str keyword_1 - unhealthy food names separated by coma
    :param str keyword_2 - healthy food names separated by coma
    """
    response = google_images_download.googleimagesdownload()   #class instantiation

    arguments_1 = {"keywords":keywords_1,
                   "limit":100,
                   "silent_mode":True,
                   "format":"jpg", 
                   "prefix":"fast_food",
                   "output_directory":os.path.abspath(os.path.join(os.getcwd(), os.pardir)),
                   "image_directory":'data_food_classifier_MG'}   #creating list of arguments

    response.download(arguments_1)   #passing the arguments to the function

    arguments_2 = {"keywords":keywords_2,
                   "limit":100,
                   "silent_mode":True,
                   "format":"jpg", 
                   "prefix":"slow_food",
                   "output_directory":os.path.abspath(os.path.join(os.getcwd(), os.pardir)),
                   "image_directory":'data_food_classifier_MG'}   #creating list of arguments
    response.download(arguments_2)   #passing the arguments to the function
