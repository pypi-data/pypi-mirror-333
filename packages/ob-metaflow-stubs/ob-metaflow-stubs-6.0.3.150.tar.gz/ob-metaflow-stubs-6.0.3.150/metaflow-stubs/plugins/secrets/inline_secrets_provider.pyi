######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.5.1+obcheckpoint(0.1.9);ob(v1)                                                    #
# Generated on 2025-03-13T17:31:16.229052                                                            #
######################################################################################################

from __future__ import annotations

import abc
import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.secrets
    import abc

from . import SecretsProvider as SecretsProvider

class InlineSecretsProvider(metaflow.plugins.secrets.SecretsProvider, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None):
        """
        Intended to be used for testing purposes only.
        """
        ...
    ...

