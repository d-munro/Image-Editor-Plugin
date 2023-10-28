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
from python.image.timestamp import Timestamp


class Image:
    """
    Contains all relevant information about a given image.

    Properties:

    """

    def __init__(self, image_file_path: str, window_name: str, rgb_color_code: tuple):
        """
        Params:
            image_file_path (str): The path to the image which the user is modifying.
            window_name (str): The title to be given to the window where users modify the image.
            rgb_color_code (tuple): The color code of all modifications being made to the image.
        """
        self._current_rectangle = Rectangle(rgb_color_code)
        self._all_rectangles = []

        self._current_image = cv2.imread(image_file_path)
        self._window_name = window_name
        self._color = rgb_color_code

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
            color = self._current_rectangle.color

            # Draw the rectangle on the image
            cv2.rectangle(
                self._current_image, vertex_1, vertex_2, color, -1)

            self._all_rectangles.append(self._current_rectangle)
            self._current_rectangle = Rectangle(self._color)

    def append_history(self, timestamp: list):
        """
        Append an item to the image's history.

        Params:
            image_timestamp (list): A mapping of the image pixels to be added to the image's history.
        """
        self._history.append(timestamp)

    def generate_timestamp(self) -> Timestamp:
        """
        Generates a timestamp of all relevant information to the current image to allow for reloading it in the future.

        Returns:
            (Timestamp): All relevant information about the current image.
        """
        timestamp = Timestamp(self._current_image)
        return timestamp
        timestamp

        self.append_history(self._current_image.copy())

    def update(self):
        """
        Updates the image which is currently being shown on the screen.
        """

        # Render the image
        cv2.namedWindow(self._window_name)
        cv2.setMouseCallback(self._window_name, self._draw_rectangle)
        cv2.imshow(self._window_name, self._current_image)

        key = cv2.waitKey(10) & 0xFF  # Return ASCII value of integer

    def undo(self):
        """
        Undo the most recent edit to the image and delete it from the image's history.
        """
        self._current_image[:] = self._history.pop()
        if self._current_rectangle_coordinates:
            self._current_rectangle_coordinates.pop()
        self.update()
