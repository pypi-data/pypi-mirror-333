######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.5.1+obcheckpoint(0.1.9);ob(v1)                                                    #
# Generated on 2025-03-13T17:31:16.210183                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ......exception import MetaflowException as MetaflowException

class CheckpointNotAvailableException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

class CheckpointException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

