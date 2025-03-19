from typing import Callable

from .._hycore.async_socket import Asyncsocket
from .._hycore.utils.triggers import Hook
from .protrols.protrol_abc import HySocketProtrol


class _HySocket:
    def __init__(self, s: Asyncsocket = None):
        self.s = s or Asyncsocket()
        self._protrols = []
        self._addon_funcs = {}  # type: dict[str, Hook]
        self._builtin_funcs = {}  # type: dict[str, Hook]

    def _init_builitin_funcs(self):
        for name in dir(self.s):
            if name.startswith("_"):
                continue

            value = getattr(self.s, name)
            if not isinstance(value, Callable):
                continue

            self._builtin_funcs[name] = Hook(value)

    def _get_function(self, name):
        if name in self._addon_funcs:
            return self._addon_funcs[name]
        elif name in self._builtin_funcs:
            return self._builtin_funcs[name]
        else:
            raise AttributeError(f"{name} is not in HySocket")

    def _exists(self, name):
        return name in self._builtin_funcs or name in self._addon_funcs

    def _add_protrol(self, protrol: HySocketProtrol):
        self._protrols.append(protrol)
        hook = self._get_function(protrol.trig_on)
        if protrol.has_pre():
            hook.pre(protrol.pre)
        if protrol.has_post():
            hook.post(protrol.post)

    def _add_addon_func(self, protrol: HySocketProtrol):
        for name, func in protrol.addon_funcs.items():
            if name not in self._addon_funcs:
                self._addon_funcs[name] = Hook(getattr(self, func))
            else:
                raise ValueError(f"Addon func {name} is already exists")

    def load_protrols(self, *protrols: HySocketProtrol):
        for protrol in protrols:
            self._add_protrol(protrol)
            self._add_addon_func(protrol)

    def __getattr__(self, function, *args, **kwargs):
        if function in self._addon_funcs:
            return self._addon_funcs[function]
        elif hasattr(self.s, function):
            return getattr(self.s, function, *args, **kwargs)
        else:
            raise AttributeError(f"{function} is not in HySocket")


class HySocket:
    def __init__(self, s: Asyncsocket = None):
        self.s = _HySocket(s)
        self.s.load_protrols()

