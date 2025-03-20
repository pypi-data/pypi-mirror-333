######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.5.1+obcheckpoint(0.1.9);ob(v1)                                                    #
# Generated on 2025-03-13T17:31:16.188888                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from .exception import MetaflowException as MetaflowException

class PyLintWarn(metaflow.exception.MetaflowException, metaclass=type):
    ...

class PyLint(object, metaclass=type):
    def __init__(self, fname):
        ...
    def has_pylint(self):
        ...
    def run(self, logger = None, warnings = False, pylint_config = []):
        ...
    ...

