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
import os
import json

from python.image.image import Image
from python.image.exceptions import ImageException


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
        self._all_modified_images = []
        self._refresh_rate = refresh_rate

    def generate_image_files_from_metadata(self, image_metadata: list, saved_image_folder_path: str) -> list:
        """
        Generates a folder of JPG image files from a list of image metadata.

        Params:
            image_metadata (list): The metadata being used to generate each image.
            saved_image_folder_path (str): The path to the folder where the images should be saved.

        Returns:
            (list): The path to each new image file generated.
        """
        new_image_file_paths = []
        for current_metadata in image_metadata:
            image = Image(self._color, self._refresh_rate)
            image.load_image_from_metadata(current_metadata)
            jpg_file_path = self.save_image(image, saved_image_folder_path)
            new_image_file_paths.append(jpg_file_path)
        return new_image_file_paths

    def _get_file_name_without_extension(self, file_path: str):
        """
        Removes the folder path and file extension from a string and returns it.
        """
        # Regex to remove the file extension and folder path from a string
        regex = "^.*\\\\(.*)\.[^\.]+$"
        filtered_name = re.findall(
            regex, file_path)[0]
        return filtered_name

    def load_image_from_jpg(self, image_file_path: str):
        """
        Loads an image into the program from a JPG file.
        """
        window_name = self._get_file_name_without_extension(image_file_path)
        self._current_image = Image(self._color, self._refresh_rate)
        self._current_image.load_image_from_jpg_file(
            image_file_path, window_name)

    def save_current_image(self, folder_path: str, file_name: str = None) -> str:
        """
        Saves the current image to the specified folder.

        Params:
            folder_path (str): The path to the folder where the image should be saved.
            custom_file_name (str, default=None): The name of the file that the image should be saved as.
                If None, the image will have the same file name as the image originally loaded into the image editor.

        Returns:
            (str): The path to the file where the image has been saved.
        """
        return self.save_image(self._current_image, folder_path, file_name=file_name)

    def save_image(self, image: Image, folder_path: str, file_name: str = None) -> str:
        """
        Saves an image to a JPG file.

        Params:
            image (Image): The image to be saved to a file.
            folder_path (str): The path to the folder where the image should be saved.
            file_name (str, default=None): The name of the file where the image should be saved.
                If None, the file name will be the original file name specified in the image's metadata.

        Returns:
            (str): The path to the file where the image has been saved.
        """
        # Create the directory if required
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        if file_name is None:
            image_metadata = image.generate_metadata()
            original_file_path = image_metadata["original_file_path"]
            original_directory_path, file_name = os.path.split(
                original_file_path)
        new_image_path = os.path.join(folder_path, file_name)
        image.save_as_jpg(new_image_path)
        return new_image_path

    def save_all_image_metadata(self, folder_path: str, json_file_name: str = "metadata.json") -> str:
        """
        Saves all image metadata to a JSON file.

        Params:
            folder_path (str): The folder where the metadata should be saved.
            json_file_name (str, default="metadata.json"): The name of the JSON file storing the image metadata.

        Returns:
            (str): The path to the JSON file where the metadata was saved.
        """
        all_metadata = [image.generate_metadata()
                        for image in self._all_modified_images]
        file_path = os.path.join(folder_path, json_file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(all_metadata, f, ensure_ascii=False, indent=4)
        return file_path

    def close_current_image(self):
        """
        Safely closes the image currently loaded into the image editor.
        """
        if self._current_image is None:
            return
        self._all_modified_images.append(self._current_image)
        self._current_image.close()
        self._current_image = None

    def close(self):
        """
        Performs all operations to safely close the image editor.
        """
        self.close_current_image()

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
        Refresh the current image window.

        Raises:
            (ImageException): If the image could not be refreshed.
        """
        try:
            if self._current_image is None:
                raise ImageException("No image is currently loaded")
            self._current_image.update()
        except ImageException as e:
            raise e
