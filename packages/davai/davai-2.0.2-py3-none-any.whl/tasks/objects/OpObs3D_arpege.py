# -*- coding: utf-8 -*-
"""
Loop on obstypes to test BatorODB+Screening independantly on each obstypes.
"""

from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex.layout.nodes import Driver, Family, LoopFamily

from tasks.assim.raw2odb.batodb import BatorODB
from .opobs.Hdirect import Hdirect
from .opobs.H import H


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arpege', ticket=t, nodes=[
            Family(tag='3dvar6h', ticket=t, nodes=[
                Family(tag='default_compilation_flavour', ticket=t, nodes=[
                    LoopFamily(tag='obstype', ticket=t,
                        loopconf='obstypes',
                        loopsuffix='.{}',
                        nodes=[
                        Family('H', ticket=t, on_error='delayed_fail', nodes=[
                            BatorODB(tag='batodb', ticket=t, **kw),
                            Hdirect(tag='hdirect', ticket=t, **kw),
                            H(tag='test_hop_with_jo', ticket=t, on_error='delayed_fail', **kw),
                            H(tag='test_adjoint', ticket=t, on_error='delayed_fail', **kw),

                            #TODO: Tests with VARBC not implemented yet in CY48
                            #H(tag='test_hop_with_jo+varbc', ticket=t, on_error='delayed_fail', **kw),
                            #H(tag='test_adjoint+varbc', ticket=t, on_error='delayed_fail', **kw),
                            ], **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

