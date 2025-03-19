import asyncio

from .protrol_abc import HySocketProtrol

from ..._hycore.neostruct import unpack_variable_length_int_from_readable


class Redirect_Protrol(HySocketProtrol):
    trig_on = 'connect'

    async def post(self, res, addr, timeout=None):
        io = self.parent.s.
