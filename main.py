# Copyright 2023 Dylan Munro
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import cv2

from python.driver import Driver
from python.hotkey.enums.predefined_hotkey import PredefinedHotkey


def draw_rectangles_and_save(image_path: str, rectangles: list, rectangle_color: tuple, output_path: str):
    """
    Draws a list of rectangle coordinates onto an image and saves it.

    Params:
        image_path (str): The path to the image where the rectangles should be drawn.
        rectangles (list(list(tuple))): List of (x, y) coordinates indicating where the rectangles should be drawn on the image.
            Each rectangle drawn should be a list of two tuples, which are the top-left and bottom-right vertices of the rectangle.
        rectangle_color (tuple): RGB code for the colour of rectangle that should be drawn on the image.
        output_path (str): The path to the file where the new image should be saved.
    """
    image = cv2.imread(image_path)
    for rectangle in rectangles:
        cv2.rectangle(image, rectangle[0], rectangle[1], rectangle_color, -1)
    cv2.imwrite(output_path, image)


def generate_images(image_modifications: dict, new_image_folder_path: str) -> list:
    """
    Modifies a given directory of images based on the specifications given in a dictionary.

    Params:
        image_modifications (dict): The modifications to be made on the images.
        new_image_folder_path (str): The path to the folder where the newly generated images should be saved.

    Returns:
        (list): The path to each new image file generated.
    """
    new_image_file_paths = []
    for image in image_modifications:
        rectangle_color = hex_to_rgb(image["rectangle_color"])
        image_path = image["image"]
        rectangle_coordinates = []
        dict_coordinates = image["coordinates"]
        for coordinate in dict_coordinates:
            vertices = []
            vertices.append((coordinate[0]["x"], coordinate[0]["y"]))
            vertices.append((coordinate[1]["x"], coordinate[1]["y"]))
            rectangle_coordinates.append(vertices)
        image_file_name = os.path.split(image_path)[1]
        if not os.path.isdir(new_image_folder_path):
            os.mkdir(new_image_folder_path)
        new_image_file_path = os.path.join(
            new_image_folder_path, image_file_name)
        draw_rectangles_and_save(
            image_path, rectangle_coordinates, rectangle_color, new_image_file_path)
        new_image_file_paths.append(new_image_file_path)
    return new_image_file_paths


def print_instructions():
    print("Hotkeys")
    print(f"{PredefinedHotkey.NEXT_IMAGE.value.key}: Move to the next image")
    print(f"{PredefinedHotkey.UNDO.value.key}: Undo your most recent action")


if __name__ == "__main__":
    print_instructions()
    driver = Driver("resources\\images", "#550000", 10)
    driver.run()

    # new_image_paths = generate_images(
    #    image_modifications, "resources\\output_images")
