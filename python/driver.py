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
import os
import queue
import sys
import traceback

from python.hotkey.hotkey_listener import HotkeyListener
from python.image.image_editor import ImageEditor
from python.hotkey.enums.predefined_hotkey import PredefinedHotkey
from python.hotkey.hotkey import Hotkey


class Driver:
    """
    Main class to drive backend program functionality.
    """

    def __init__(self, image_folder_path: str, editing_color: str, refresh_rate: int, output_folder_path: str) -> dict:
        """
        Params:
            image_folder_path (str): The path to the folder containing the images to be modified.
            editing_color (str): Hexadecimal value of the color being used to modify the image.
            refresh_rate (int): Refresh rate of on-screen images.
            output_folder_path (str): The path to the folder where all outputs should be saved.
        """
        self._image_folder_path = image_folder_path
        self._image_editor = ImageEditor(editing_color, refresh_rate)
        if not os.path.exists(output_folder_path):
            os.mkdir(output_folder_path)
        self._output_folder_path = output_folder_path

        self._hotkey_queue = queue.Queue()
        self._hotkey_listener_thread = HotkeyListener(self._hotkey_queue)
        self._hotkey_listener_thread.daemon = True

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

    def _execute_hotkey(self, hotkey: Hotkey):
        """
        Executes the desired functionality of a given hotkey.

        Raises:
            (UserWarning): If an unexpected event occured.
        """
        try:
            if hotkey.key == PredefinedHotkey.NEXT_IMAGE.value.key:
                self._image_editor.save_current_image(self._output_folder_path)
                self._image_editor.close_current_image()
            elif hotkey.key == PredefinedHotkey.CLOSE_PROGRAM.value.key:
                self.shutdown(
                    message=f"Detected key {hotkey.key.name} - Terminating program")
            elif hotkey.key == PredefinedHotkey.UNDO.value.key:
                self._image_editor.undo()
        except UserWarning as e:
            raise e

    def shutdown(self, message: str = None, exception: Exception = None):
        """
        Performs all necessary actions to safely shutdown the program.

        Params:
            message (str, default=None): A message to be outputted to the user upon shutdown.
            exception (Exception, default=None): The exception which caused the program to shutdown.
        """
        if not message is None:
            print(message)
        if not exception is None:
            traceback.print_exception(exception)
        # self._image_editor.save_all_image_metadata(self._output_folder_path)
        self._image_editor.close()
        self._hotkey_listener_thread.stop()
        self._hotkey_listener_thread.join()
        sys.exit()

    def run(self):
        """
        Main loop used to run the program.
        """
        jpg_file_paths = self.get_all_jpg_file_paths(self._image_folder_path)
        if len(jpg_file_paths) == 0:
            return
        self._hotkey_listener_thread.start()
        for image_file_path in jpg_file_paths:
            self._image_editor.load_image_from_jpg(image_file_path)
            current_hotkey = None
            while current_hotkey is None or current_hotkey.key != PredefinedHotkey.NEXT_IMAGE.value.key:

                # Must refresh the image before parsing the hotkey in case the hotkey indicates to close the image
                self._image_editor.refresh()

                if not self._hotkey_queue.empty():
                    try:
                        current_hotkey = self._hotkey_queue.get()
                        self._execute_hotkey(current_hotkey)
                    except queue.Empty:
                        pass
                    except UserWarning as e:
                        print(e)
                    except Exception as e:
                        self.shutdown(
                            message="Unexpected exception occured - Terminating program\n\n", exception=e)

        shutdown_message = f"\nFinished editing all images\nAll images have been written to {self._output_folder_path}"
        self.shutdown(shutdown_message)
