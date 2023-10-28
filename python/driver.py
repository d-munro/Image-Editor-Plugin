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

"""
Main module responsible for driving all backend activity for the program.
"""

import re
import json
import os

from python.hotkey.keyboard_handler import HotkeyHandler
from python.image.image_handler import ImageHandler
from python.image.image import Image
from python.utils import hex_to_rgb


class Driver:
    """
    Main class to drive backend program functionality.
    """

    def __init__(self, image_folder_path: str, output_json_file_path: str, hex_color: str = "#000000") -> dict:
        """
        Params:
            image_folder_path (str): The path to the folder containing the images to be modified.
            output_json_file_path (str): The path to the JSON file containing all necessary information to modify the images at a future time.
            hotkey_delay (float, default=0): The amount of seconds to wait before enabling hotkeys again after a hotkey is entered.
            hex_color (str, default="#000000"): The hexadecimal value for the colour of the rectangles being overlayed on the images.

        Returns:
            (dict): The modifications to be made to the given images.
        """
        self._image_folder_path = image_folder_path
        self._output_json_file_path = output_json_file_path
        self._hex_color = hex_to_rgb(hex_color)
        self._current_image = None

        # Event handlers
        self._hotkey_handler = HotkeyHandler()
        self._image_handler = ImageHandler()

    def get_all_jpg_file_paths(self, folder_path: str) -> list:
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

    def run(self):
        """
        Main loop used to run the program.
        """

        jpg_file_paths = self.get_all_jpg_file_paths(self._image_folder_path)
        if len(jpg_file_paths) == 0:
            return

        edited_images = []
        for image_file_path in jpg_file_paths:

            # Regex to remove the file extension and folder path from a string
            filter_extension_regex = "^.*\\\\(.*)\.[^\.]+$"
            window_name = re.findall(
                filter_extension_regex, image_file_path)[0]
            current_image = Image(
                image_file_path, window_name, self._hex_color)

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
