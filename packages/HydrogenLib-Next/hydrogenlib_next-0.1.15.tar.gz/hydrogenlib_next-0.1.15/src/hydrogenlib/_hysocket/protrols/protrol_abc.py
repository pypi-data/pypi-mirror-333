from abc import ABC

from . import HySocket


class HySocketProtrol(ABC):
    parent: HySocket

    trig_on = None
    addon_funcs = []

    def __init__(self, parent: HySocket, *args, **kwargs):
        self.parent = parent

    async def pre(self, *args, **kwargs):
        ...

    async def post(self, *args, **kwargs):
        ...

    @classmethod
    def has_pre(cls):
        return cls.pre is not HySocketProtrol.pre

    @classmethod
    def has_post(cls):
        return cls.post is not HySocketProtrol.post
