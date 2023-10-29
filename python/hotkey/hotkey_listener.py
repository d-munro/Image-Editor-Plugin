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
from queue import Queue
import threading

from python.hotkey.enums.predefined_hotkey import PredefinedHotkey


class HotkeyListener(threading.Thread):
    """
    Listens for any predefined hotkeys being entered by the user.
    """

    def __init__(self, hotkey_queue: Queue):
        """
        Params:
            hotkey_queue (Queue): Queue of hotkeys pending execution. Shared between the HotkeyListener and Driver classes.
        """
        super().__init__()
        self._hotkey_queue = hotkey_queue
        self._stop_event = threading.Event()

        self._keys_to_hotkeys = self._generate_hotkeys()
        self._hotkeys_to_delays = self._generate_hotkeys_to_delays()

    def _generate_hotkeys(self):
        """
        Returns:
            (dict): Dictionary mapping each hotkey to its associated enum value.
        """
        keys_to_hotkeys = dict()
        for key in PredefinedHotkey:
            keys_to_hotkeys[key.value.key] = key
        return keys_to_hotkeys

    def _generate_hotkeys_to_delays(self) -> dict:
        """
        Returns:
            (dict): Dictionary mapping each predefined hotkey to its associated delay.
        """
        hotkeys_to_delays = {}
        for entry in PredefinedHotkey:
            hotkeys_to_delays[entry.value.key] = entry.value.delay
        return hotkeys_to_delays

    def run(self):
        """
        Listens for hotkeys and adds them to the queue when detected.
        """
        while not self._stop_event.is_set():
            keyboard_event = keyboard.read_event()
            key = keyboard_event.name
            if key in self._keys_to_hotkeys:
                self._hotkey_queue.put(self._keys_to_hotkeys.get(key))

    def stop(self):
        """
        Stops the thread.
        """
        self._stop_event.set()
