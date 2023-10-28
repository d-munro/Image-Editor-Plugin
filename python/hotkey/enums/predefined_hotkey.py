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

from enum import Enum
from python.hotkey.hotkey import Hotkey
from python.hotkey.enums.key import Key


class PredefinedHotkey(Enum):
    """
    All hotkey bindings for the program.
    """
    CLOSE_PROGRAM = Hotkey(
        Key.ESC, 1)  # Terminates the program without saving anything
    NEXT_IMAGE = Hotkey(Key.D, 0.125)
    UNDO = Hotkey(Key.CTRL_Z, 0.125)
