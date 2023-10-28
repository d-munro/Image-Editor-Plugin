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


class Driver:
    """
    Main class to drive backend program functionality.
    """

    def __init__(self, image_folder_path: str, editing_color: tuple, refresh_rate: int) -> dict:
        """
        Params:
            image_folder_path (str): The path to the folder containing the images to be modified.
            hex_color (tuple): RGB code of the initial color being used to edit the images.
            refresh_rate (int): The number of milliseconds to wait before refreshing the images.

        Returns:
            (dict): The modifications to be made to the given images.
        """
        self._image_folder_path = image_folder_path
        self._hotkey_handler = HotkeyHandler()
        self._image_handler = ImageHandler(editing_color, refresh_rate)

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
            load_next_image = False
            self._image_handler.load_image(image_file_path)
            while not load_next_image:
                load_next_image = self._image_handler.refresh()

                # keyboard_event = keyboard.read_event()
                #    hotkey_handler.handle_event(keyboard_event)

    def write_images_to_json(self, json_file_path: str):
        """
        Writes all relevant information about the images to a JSON file.
        """
        all_images = self._image_handler.get_all_images()
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(all_images, f, ensure_ascii=False, indent=4)
