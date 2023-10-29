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
Module responsible for modifying and updating on-screen images.
"""

import re
import cv2

from python.image.image import Image


class ImageEditor:
    """
    Modifies and updates on-screen images.
    """

    def __init__(self, editing_color: str, refresh_rate: int):
        """
        Params:
            editing_color (str): Hexadecimal value of the colour currently being used to modify the on-screen image.
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

    def undo(self):
        """
        Undoes the most recent action.
        
        Raises:
            (UserWarning): If there was nothing to undo.
        """
        try:
            self._current_image.undo()
        except UserWarning as e:
            raise e

    def refresh(self):
        """
        Refreshes the active window.
        """
        self._current_image.update()
        cv2.waitKey(self._refresh_rate)
