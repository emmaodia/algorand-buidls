import typing as t
from algopy import Box, arc4, ARC4Contract, String


class MyContract(ARC4Contract):
    def __init__(self) -> None:
        self.box_b = Box(arc4.String, key=b"BOX_B")

    @arc4.abimethod
    def hello_world(self, name: String) -> bool:
        self.box_b.value = arc4.String("Hello, " + name)
        return True

    @arc4.abimethod
    def read_message(self) -> arc4.String:
        return self.box_b.value
