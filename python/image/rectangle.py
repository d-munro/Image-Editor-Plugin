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

class Rectangle:
    """
    Rectangle-like object which is drawn on a given image.
    """

    def __init__(self, color: str):
        """
        Params:
            color (str): The hexadecimal color code of the rectangle.
        """
        self._vertices = []
        self._color = color

    @property
    def vertices(self) -> list:
        """
        A list of all vertices composing the rectangle stored as tuples.
            The format of the tuples is (x-coordinate, y-coordinate).
        """
        return self._vertices

    @property
    def color(self) -> str:
        """
        The hexadecimal color code of the rectangle.
        """
        return self._color

    def add_vertex(self, x: int, y: int):
        """
        Adds a vertex to the rectangle.

        Params:
            x (int): The x-coordinate of the vertex.
            y (int): The y-coordinate of the vertex.
        """
        self._vertices.append((x, y))

    def num_vertices(self) -> int:
        """
        Returns:
            (int): The number of vertices currently in the rectangle.
        """
        return len(self._vertices)

    def pop_vertex(self) -> list:
        """
        Removes the most recently added vertex from the list of vertices.
        """
        self._vertices = self._vertices.pop()
        return self._vertices

    def to_dict(self) -> dict:
        """
        Returns:
            (dict): Dictionary representation of the rectangle's metadata.
        """
        metadata = {}
        vertices_dict = []
        for vertex in self._vertices:
            vertex_dict = {}
            vertex_dict["x"], vertex_dict["y"] = vertex
            vertices_dict.append(vertex_dict)
        metadata["vertices"] = vertices_dict
        metadata["color"] = self._color
        return metadata
