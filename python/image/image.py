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

from python.image.rectangle import Rectangle
from python.image.exceptions import ImageException


class Image:
    """
    Stores all metadata about an existing image.
    """

    def __init__(self, hex_color_code: str, refresh_rate: int):
        """
        Params:
            refresh_rate (int): The number of milliseconds to wait before refreshing the image.
            hex_color_code (str): The color being used to modify the image.
        """
        self._refresh_rate = refresh_rate
        self._current_rectangle = Rectangle(hex_color_code)
        self._all_rectangles = []
        self._history = []
        self._color = hex_color_code
        self._is_generated = False

        self._original_file_path = None
        self._current_image = None
        self._window_name = None

    def close(self):
        """
        Closes the image.
        """
        cv2.destroyWindow(self._window_name)

    def _draw_rectangle(self, event, x, y, flags, params):
        """
        Function passed to cv2's setMouseCallBack function to draw rectangles on the current image.

        Params:
            event: The mouse event.
            x (int): The x coordinate of the mouse at the time of the event.
            y (int): The y coordinate of the mouse at the time of the event.
        """

        # Store the starting point when the left button is pressed
        if event == cv2.EVENT_LBUTTONDOWN:
            self._current_rectangle.add_vertex(x, y)

        # Store the ending point when the left button is released
        elif event == cv2.EVENT_LBUTTONUP:

            self._current_rectangle.add_vertex(x, y)
            vertex_1, vertex_2 = self._current_rectangle.vertices[
                0], self._current_rectangle.vertices[1]
            color = self._hex_to_rgb(self._current_rectangle.color)

            # Must save the image before updating it with the new rectangle in case of undoing the action
            self._history.append(self.generate_metadata())

            # Draw the rectangle on the image
            cv2.rectangle(
                self._current_image, vertex_1, vertex_2, color, -1)

            self._all_rectangles.append(self._current_rectangle)
            self._current_rectangle = Rectangle(self._color)

    def generate_metadata(self) -> dict:
        """
        Generates a dictionary of the image's metadata which can be used to reload it in the future.

        Returns:
            (dict): All relevant information about the current image.
        """
        metadata = {}
        metadata["original_file_path"] = self._original_file_path
        metadata["window_name"] = self._window_name
        metadata["image"] = self._current_image.copy()
        if not self._all_rectangles is None:
            metadata["rectangles"] = [
                rectangle.to_dict() for rectangle in self._all_rectangles]
        return metadata

    def _load_rectangles(self, metadata) -> list:
        """
        Loads all rectangles from the image metadata into the program.
        """
        all_rectangles = []
        rectangle_list = metadata["rectangles"]
        if not rectangle_list is None:
            for rectangle in rectangle_list:
                color = rectangle["color"]
                generated_rectangle = Rectangle(color)
                vertices = rectangle["vertices"]
                for vertex in vertices:
                    generated_rectangle.add_vertex(vertex["x"], vertex["y"])
                all_rectangles.append(generated_rectangle)
        return all_rectangles

    def load_image_from_jpg_file(self, jpg_file_path: str, window_name: str):
        """
        Loads an imge from a JPG file.

        Params:
            jpg_file_path (str): The path to the image which the user is modifying.
            window_name (str): The title to be given to the window where users modify the image.
        """
        self._original_file_path = jpg_file_path
        self._current_image = cv2.imread(jpg_file_path)
        self._window_name = window_name
        self._is_generated = True

    def load_image_from_metadata(self, metadata: dict):
        """
        Loads an image from previously generated image metadata.

        Params:
            metadata (dict): Metadata describing the image. It should have the following keys:
                1) original_file_path: The path to the original file containing the image, before any modifications.
                2) window_name: The title of the window where the image will be displayed.
                3) image: The array of RGB values for all pixels in the image.
                4) rectangles (optional): The coordinates of any rectangles which have been overlayed onto the image.
        """
        self._original_file_path = metadata["original_file_path"]
        self._window_name = metadata["window_name"]
        self._current_image = metadata["image"]
        self._all_rectangles = self._load_rectangles(metadata)
        self._is_generated = True

    def _hex_to_rgb(self, hex_code: str) -> tuple:
        """
        Convert a hexadecimal color to an R, G, B) tuple.

        Params:
            hex_code (str): The code to be converted into RGB.
                For example: #FFFFFF.

        Returns:
            (tuple): The (R, G, B) colour code of the hexadecimal string.
        """
        hex_color = hex_code.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def save_as_jpg(self, jpg_file_path: str):
        """
        Saves the current image to a jpg file.
        """
        cv2.imwrite(jpg_file_path, self._current_image)

    def update(self):
        """
        Updates the image which is currently being shown on the screen.

        Raises:
            (ImageException): If the image has not been generated yet.
        """
        if not self._is_generated:
            raise ImageException(
                "The image has not yet been loaded from a file or metadata")
        cv2.namedWindow(self._window_name)
        cv2.setMouseCallback(self._window_name, self._draw_rectangle)
        cv2.imshow(self._window_name, self._current_image)
        cv2.waitKey(self._refresh_rate)

    def undo(self):
        """
        Undo the most recent edit to the image and delete it from the image's history.

        Raises:
            (UserWarning): If the most recent action could not be undone.
        """
        if len(self._history) == 0:
            raise UserWarning("Image history was already empty")
        metadata = self._history.pop()
        self.load_image_from_metadata(metadata)
