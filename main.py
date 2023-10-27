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

import cv2
import os
import re
import keyboard
import time
import json

from enums.hotkeys import Hotkey

# Lists to store the rectangles and current drawing state
current_rectangle_points = []


def hex_to_rgb(hex_color) -> tuple:
    """
    Convert a hexadecimal color to an (R, G, B) tuple.
    """
    hex_color = hex_color.lstrip(
        '#')  # Remove the hash at the start if it's there
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def draw_rectangle(event, x, y, flags, params: dict):
    """
    Draws a rectangle on the given image.

    Params:
        event: The mouse event.
        x (int): The x coordinate of the mouse at the time of the event.
        y (int): The y coordinate of the mouse at the time of the event.
        params (dict): Any other parameters passed to the function.
    """
    current_image = params["image"]
    all_rectangle_coordinates = params["all_coordinates"]
    color = params["color"]

    if event == cv2.EVENT_LBUTTONDOWN:
        # Store the starting point when the left button is pressed
        current_rectangle_points.append({"x": x, "y": y})

    elif event == cv2.EVENT_LBUTTONUP:
        # Store the ending point when the left button is released
        current_rectangle_points.append({"x": x, "y": y})
        params["image_history"].append(current_image.copy())

        # Draw the rectangle on the image
        point_1 = (current_rectangle_points[0]
                   ["x"], current_rectangle_points[0]["y"])
        point_2 = (current_rectangle_points[1]
                   ["x"], current_rectangle_points[1]["y"])
        cv2.rectangle(
            current_image, point_1, point_2, color, -1)
        all_rectangle_coordinates.append(
            (current_rectangle_points[0], current_rectangle_points[1]))
        current_rectangle_points.clear()


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


def edit_images(image_folder_path: str, output_json_file_path: str, hotkey_delay: float = 0, hex_color: str = "#000000") -> dict:
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
    color = hex_to_rgb(hex_color)

    jpg_file_paths = get_all_jpg_file_paths(image_folder_path)
    if len(jpg_file_paths) == 0:
        return

    edited_images = []
    for jpg_file_path in jpg_file_paths:
        current_image_to_rectangle_coordinates = {}
        current_jpg_rectangle_coordinates = []
        original_image = cv2.imread(jpg_file_path)
        current_image = original_image.copy()
        image_history = [original_image.copy()]
        last_hotkey_time = 0

        while True:

            # Regex to remove the file extension and folder path from a string
            filter_extension_regex = "^.*\\\\(.*)\.[^\.]+$"
            window_name = re.findall(filter_extension_regex, jpg_file_path)[0]

            # Render the image
            cv2.namedWindow(window_name)
            cv2.setMouseCallback(window_name, draw_rectangle,
                                 param={"image": current_image, "color": color,
                                        "all_coordinates": current_jpg_rectangle_coordinates, "image_history": image_history})
            cv2.imshow(window_name, current_image)
            key = cv2.waitKey(10) & 0xFF  # Return ASCII value of integer

            # Load the next image
            if keyboard.is_pressed(Hotkey.NEXT_IMAGE.value) and time.time() - last_hotkey_time > hotkey_delay:
                break

            # Undo the most recent action
            elif keyboard.is_pressed(Hotkey.UNDO.value) and time.time() - last_hotkey_time > hotkey_delay:
                current_image[:] = image_history.pop()
                if current_jpg_rectangle_coordinates:
                    current_jpg_rectangle_coordinates.pop()
                last_hotkey_time = time.time()

        current_image_to_rectangle_coordinates["image"] = jpg_file_path
        current_image_to_rectangle_coordinates["coordinates"] = current_jpg_rectangle_coordinates
        current_image_to_rectangle_coordinates["rectangle_color"] = hex_color
        edited_images.append(current_image_to_rectangle_coordinates)
        cv2.destroyAllWindows()

    to_json(edited_images, json_file_path=output_json_file_path)
    return edited_images


def print_instructions():
    print("Hotkeys")
    print(f"{Hotkey.NEXT_IMAGE.value}: Move to the next image")
    print(f"{Hotkey.UNDO.value}: Undo your most recent action")


if __name__ == "__main__":
    print_instructions()
    image_modifications = edit_images("resources\\images",
                                      "resources\\output.json", hex_color="#550000", hotkey_delay=0.125)
    new_image_paths = generate_images(
        image_modifications, "resources\\output_images")
