######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.5.1+obcheckpoint(0.1.9);ob(v1)                                                    #
# Generated on 2025-03-13T17:31:16.207961                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.monitor


class DebugMonitor(metaflow.monitor.NullMonitor, metaclass=type):
    @classmethod
    def get_worker(cls):
        ...
    ...

class DebugMonitorSidecar(object, metaclass=type):
    def __init__(self):
        ...
    def process_message(self, msg):
        ...
    ...

