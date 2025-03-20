# -*- coding: utf-8 -*-

from mod.common.component.baseComponent import BaseComponent
from typing import Tuple

class ParticleEntityBindComp(BaseComponent):
    def Bind(self, isClientEntity, bindEntityId, offset, rot=False, correction=False):
        # type: (bool, str, Tuple[float,float,float], Tuple[float,float,float], bool) -> bool
        """
        绑定entity
        """
        pass

