from django.shortcuts import get_object_or_404
from app.settings import BASE_DIR
import base64
from PIL import Image
import os
from time import perf_counter


def get_image_data(model, img_id):
    image_path = get_object_or_404(model, id=img_id).image.url
    image_path = str(BASE_DIR) + image_path

    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    return image_data
