from collections import defaultdict

from imuthes import Singleton
from sqlalchemy.orm import Session

import inspect

from hakisto import Logger

logger = Logger("imuthes.ansible.deferrer")

Logger.register_excluded_source_file(inspect.currentframe().f_code.co_filename)


class Deferrer(Singleton):

    _data = []

    def append(self, item):
        self._data.append(item)

    def execute(self, engine) -> int:
        count = 0
        with Session(engine) as session:
            for item in self._data:
                r = item(session)
                try:
                    count += len(r)
                    logger.debug(f"Added {len(r)} records")
                except TypeError:
                    count += 1
                    logger.debug(f"Added 1 record")
            session.commit()
        self._data.clear()
        return count
