######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.5                                                                                 #
# Generated on 2025-03-13T17:07:28.459823                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...exception import MetaflowException as MetaflowException

class AirflowException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

class NotSupportedException(metaflow.exception.MetaflowException, metaclass=type):
    ...

