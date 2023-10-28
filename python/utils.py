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
A library of various useful utility functions.
"""


def hex_to_rgb(hex_code: str) -> tuple:
    """
    Convert a hexadecimal color to an (R, G, B) tuple.

    Params:
        hex_code (str): The code to be converted into RGB.
            For example: #FFFFFF.

    Returns:
        (tuple): The (R, G, B) colour code of the hexadecimal string.
    """
    hex_color = hex_code.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
