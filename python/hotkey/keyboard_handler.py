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

import keyboard
import time
import sys

from python.hotkey.enums.predefined_hotkey import PredefinedHotkey
from python.image.image import Image


class HotkeyHandler:
    """
    Event handler for all hotkey-related operations.
    """

    def __init__(self):
        self._all_hotkeys = self._generate_hotkeys()
        # Lists to store the rectangles and current drawing state
        self._current_rectangle_points = []
        self._current_image = []

    @property
    def current_image(self) -> list:
        return self._current_image

    @current_image.setter
    def current_image(self, image: list):
        self._current_image = image

    def _generate_hotkeys(self):
        keys_to_hotkeys = dict()
        for key in PredefinedHotkey:
            keys_to_hotkeys[key.value.key] = key.value
        return keys_to_hotkeys

    def handle_event(self, event: keyboard.KeyboardEvent):
        """
        Handles all keyboard-related events.
        """

        # Load the next image
        # if keyboard.is_pressed(Hotkey.NEXT_IMAGE.key.value) and time.time() - last_hotkey_time > hotkey_delay:
        #    break

        # Undo the most recent action
        # elif keyboard.is_pressed(Hotkey.UNDO.key.value) and time.time() - last_hotkey_time > hotkey_delay:
        #    current_image[:] = image_history.pop()
        #    if current_jpg_rectangle_coordinates:
        #        current_jpg_rectangle_coordinates.pop()
        #    last_hotkey_time = time.time()

        try:
            key = event.name
            hotkey = self._all_hotkeys.get(key)

            # Check if enough time has passed to run the hotkey
            hotkey_delay = hotkey.delay
            most_recent_call = hotkey.most_recent_trigger
            sufficient_time_passed = time.time() - most_recent_call > hotkey_delay
            if not sufficient_time_passed:
                return

            # Handle the hotkey
            if key == PredefinedHotkey.NEXT_IMAGE:
                pass
            elif key == PredefinedHotkey.UNDO:
                self.undo()
                self.update_image()
                hotkey.most_recent_trigger = time.time()
                self._all_hotkeys[key] = hotkey

            elif key == PredefinedHotkey.CLOSE_PROGRAM:
                print("Terminating program")
                sys.exit(0)

            # Update the time that the hotkey was most recently executed

        except AttributeError as e:
            raise e
