######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.5.1+obcheckpoint(0.1.9);ob(v1)                                                    #
# Generated on 2025-03-13T17:31:16.210856                                                            #
######################################################################################################

from __future__ import annotations

import typing
import metaflow
if typing.TYPE_CHECKING:
    import metaflow.exception
    import metaflow

from ......exception import MetaflowException as MetaflowException
from .core import resolve_root as resolve_root

TYPE_CHECKING: bool

class UnresolvableDatastoreException(metaflow.exception.MetaflowException, metaclass=type):
    ...

def init_datastorage_object():
    ...

def resolve_storage_backend(pathspec: typing.Union[str, "metaflow.Task"] = None):
    ...

