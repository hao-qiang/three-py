
from ...structure import NoneAttribute
from ...math import Vector2, Vector3, Vector4, Color, Matrix3, Matrix4

class WgpuUniform(NoneAttribute):

    def __init__(self, name, value = None) -> None:
        
        self.name = name
        self.value = value

        self.boundary = 0
        self.itemSize = 0

        self._offset = 0

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, v):
        self._offset = int(v)

    def setValue( self, value ):
        self.value = value


    def getValue(self):
        return self.value


class FloatUniform(WgpuUniform):

    def __init__(self, name, value=0) -> None:
        super().__init__(name, value)

        self.boundary = 4
        self.itemSize = 1

class Vector2Uniform(WgpuUniform):

    def __init__(self, name, value=None) -> None:
        super().__init__(name, value or Vector2())

        self.boundary = 8
        self.itemSize = 2

class Vector3Uniform(WgpuUniform):

    def __init__(self, name, value=None) -> None:
        super().__init__(name, value or Vector3())

        self.boundary = 16
        self.itemSize = 3


class Vector4Uniform(WgpuUniform):

    def __init__(self, name, value=None) -> None:
        super().__init__(name, value or Vector4())

        self.boundary = 16
        self.itemSize = 4


class ColorUniform(WgpuUniform):

    def __init__(self, name, value=None) -> None:
        super().__init__(name, value or Color())

        self.boundary = 16
        self.itemSize = 3

class Matrix3Uniform(WgpuUniform):

    def __init__(self, name, value=None) -> None:
        super().__init__(name, value or Matrix3())

        self.boundary = 48
        self.itemSize = 12


class Matrix4Uniform(WgpuUniform):

    def __init__(self, name, value=None) -> None:
        super().__init__(name, value or Matrix4())

        self.boundary = 64
        self.itemSize = 16


