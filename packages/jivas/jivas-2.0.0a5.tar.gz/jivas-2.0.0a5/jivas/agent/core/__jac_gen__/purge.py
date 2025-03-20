from __future__ import annotations
from jaclang import *
import typing
if typing.TYPE_CHECKING:
    import logging
else:
    logging, = jac_import('logging', 'py')
if typing.TYPE_CHECKING:
    import traceback
else:
    traceback, = jac_import('traceback', 'py')
if typing.TYPE_CHECKING:
    from logging import Logger
else:
    Logger, = jac_import('logging', 'py', items={'Logger': None})

class purge(Walker):
    logger: static[Logger] = logging.getLogger(__name__)

    @with_entry
    def delete(self, here: object) -> None:
        self.logger.debug('deleting object: {here}')
        self.visit(here.refs())
        Jac.destroy(here)