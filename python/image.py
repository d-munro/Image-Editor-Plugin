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


class Image:
    """
    Responsible for all operations relating to the image.
    """

    def __init__(self, image_file_path: str, window_name: str, hex_color: str):

        self._current_rectangle_coordinates = []
        self._all_rectangle_coordinates = []

        self._original_image = cv2.imread(image_file_path)
        self._window_name = window_name
        self._current_image = self._original_image.copy()
        self._history = [self._original_image.copy()]
        self._color = self.hex_to_rgb(hex_color)

    def hex_to_rgb(self, hex_color) -> tuple:
        """
        Convert a hexadecimal color to an (R, G, B) tuple.
        """
        hex_color = hex_color.lstrip(
            '#')  # Remove the hash at the start if it's there
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def draw_rectangle(self, event, x, y, flags, params: dict):
        """
        Draws a rectangle on the given image.

        Params:
            event: The mouse event.
            x (int): The x coordinate of the mouse at the time of the event.
            y (int): The y coordinate of the mouse at the time of the event.
            params (dict): Any other parameters passed to the function.
        """

        if event == cv2.EVENT_LBUTTONDOWN:
            # Store the starting point when the left button is pressed
            self._current_rectangle_coordinates.append({"x": x, "y": y})

        elif event == cv2.EVENT_LBUTTONUP:
            # Store the ending point when the left button is released
            self._current_rectangle_coordinates.append({"x": x, "y": y})

            # Draw the rectangle on the image
            point_1 = (self._current_rectangle_coordinates[0]
                       ["x"], self._current_rectangle_coordinates[0]["y"])
            point_2 = (self._current_rectangle_coordinates[1]
                       ["x"], self._current_rectangle_coordinates[1]["y"])
            cv2.rectangle(
                self._current_image, point_1, point_2, self._color, -1)
            self._all_rectangle_coordinates.append(
                (self._current_rectangle_coordinates[0], self._current_rectangle_coordinates[1]))
            self.append_history(self._current_image.copy())
            self._current_rectangle_coordinates.clear()

    def append_history(self, timestamp: list):
        """
        Append an item to the image's history.
        """
        self._history.append(timestamp)

    def update(self):
        """
        Updates the image which is currently being shown on the screen.
        """

        # Render the image
        cv2.namedWindow(self._window_name)
        cv2.setMouseCallback(self._window_name, self.draw_rectangle)
        cv2.imshow(self._window_name, self._current_image)

        key = cv2.waitKey(10) & 0xFF  # Return ASCII value of integer

    def undo(self):
        """
        Removes the most recent edit from the image.
        """
        self._current_image[:] = self._history.pop()
        if self._current_rectangle_coordinates:
            self._current_rectangle_coordinates.pop()
        self.update()
