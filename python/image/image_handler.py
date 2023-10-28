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

import re
import cv2

from python.image.image import Image
from python.hotkey.enums.predefined_hotkey import PredefinedHotkey


class ImageHandler:
    """
    Event handler responsible for performing all image-related actions.
    """

    def __init__(self, editing_color: tuple, refresh_rate: int):
        """
        Params:
            editing_color (tuple): RGB color code of the initial colour being used to edit the images.
            refresh_rate (int): The number of miliseconds to wait before refreshing the current image.
        """
        self._current_image = None
        self._color = editing_color
        # List of all modifications made to the images.
        self._modifications = []
        self._refresh_rate = refresh_rate

    def load_image(self, image_file_path: str):
        """
        Loads an image into the program.

        Params:
            image_file_path (str): The path to the image JPG file.
        """
        # Regex to remove the file extension and folder path from a string
        filter_extension_regex = "^.*\\\\(.*)\.[^\.]+$"

        window_name = re.findall(
            filter_extension_regex, image_file_path)[0]
        self._current_image = Image(
            image_file_path, window_name, self._color)

    def refresh(self) -> bool:
        """
        Refreshes the image.

        Returns:
            (bool): True if the next image should be loaded, False otherwise.
        """
        self._current_image.update()
        cv2.waitKey(self._refresh_rate)
        key = "test"
        if key == PredefinedHotkey.NEXT_IMAGE:
            print("read")
            # current_image_to_rectangle_coordinates["image"] = jpg_file_path
            # current_image_to_rectangle_coordinates["coordinates"] = current_jpg_rectangle_coordinates
            # current_image_to_rectangle_coordinates["rectangle_color"] = hex_color
            # edited_images.append(current_image_to_rectangle_coordinates)
            # cv2.destroyAllWindows()
            return True
        return False
