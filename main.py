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
import re
import keyboard
import json
import cv2

from python.hotkey_handler import HotkeyHandler
from enums.predefined_hotkey import PredefinedHotkey
from python.image import Image


def get_all_jpg_file_paths(folder_path: str) -> list:
    """
    Returns a list of all JPG files in a folder.
    """
    jpg_file_paths = []
    all_files = os.listdir(folder_path)
    for file_name in all_files:
        if not re.findall(".*(\.jpg)$", file_name) is None:
            file_path = os.path.join(folder_path, file_name)
            jpg_file_paths.append(file_path)
    return jpg_file_paths


def to_json(edited_images: dict, json_file_path: str):
    """
    Writes the edited images to a JSON file.
    """
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(edited_images, f, ensure_ascii=False, indent=4)


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


def edit_images(image_folder_path: str, output_json_file_path: str, hex_color: str = "#000000") -> dict:
    """
    Provides an interface for editing images and writes the modifications to a JSON file.

    Params:
        image_folder_path (str): The path to the folder containing the images to be modified.
        output_json_file_path (str): The path to the JSON file containing all necessary information to modify the images at a future time.
        hotkey_delay (float, default=0): The amount of seconds to wait before enabling hotkeys again after a hotkey is entered.
        hex_color (str, default="#000000"): The hexadecimal value for the colour of the rectangles being overlayed on the images.

    Returns:
        (dict): The modifications to be made to the given images.
    """
    hotkey_handler = HotkeyHandler()

    jpg_file_paths = get_all_jpg_file_paths(image_folder_path)
    if len(jpg_file_paths) == 0:
        return

    edited_images = []
    for image_file_path in jpg_file_paths:

        # Regex to remove the file extension and folder path from a string
        filter_extension_regex = "^.*\\\\(.*)\.[^\.]+$"
        window_name = re.findall(filter_extension_regex, image_file_path)[0]
        current_image = Image(image_file_path, window_name, hex_color)

        while True:
            try:
                current_image.update()
                # keyboard_event = keyboard.read_event()
            #    hotkey_handler.handle_event(keyboard_event)
            except AttributeError:
                #    print("error")
                pass

        current_image_to_rectangle_coordinates["image"] = jpg_file_path
        current_image_to_rectangle_coordinates["coordinates"] = current_jpg_rectangle_coordinates
        current_image_to_rectangle_coordinates["rectangle_color"] = hex_color
        edited_images.append(current_image_to_rectangle_coordinates)
        cv2.destroyAllWindows()

    to_json(edited_images, json_file_path=output_json_file_path)
    return edited_images


def print_instructions():
    print("Hotkeys")
    print(f"{PredefinedHotkey.NEXT_IMAGE.value}: Move to the next image")
    print(f"{PredefinedHotkey.UNDO.value}: Undo your most recent action")


if __name__ == "__main__":
    print_instructions()
    image_modifications = edit_images("resources\\images",
                                      "resources\\output.json", hex_color="#550000")
    new_image_paths = generate_images(
        image_modifications, "resources\\output_images")
