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


from python.hotkey.enums.key import Key


class Hotkey:
    """
    Creates a hotkey to interact with the program more easily.
    """

    def __init__(self, key: Key, delay: float):
        self._key = key
        self._delay = delay
        self._most_recent_trigger = 0

    @property
    def key(self) -> Key:
        """
        The unique key to trigger the hotkey.
        """
        return self._key

    @property
    def delay(self) -> float:
        """
        The amount of time in seconds which must be waited before the given hotkey can be used again.
        """
        return self._delay

    @property
    def most_recent_trigger(self) -> float:
        """
        The timestamp in seconds of the most recent time that the hotkey was triggered.
        """
        return self._most_recent_trigger

    @most_recent_trigger.setter
    def most_recent_trigger(self, new_timestamp: float):
        """
        Params:
            new_timestamp (float): The timestamp in seconds of the hotkey's most recent trigger.
        """
        self._most_recent_trigger = new_timestamp
