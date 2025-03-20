# ------------------------------------------------------------------------------
#  Imuthes by NetLink Consulting GmbH
#
#  Copyright (c) 2025. Bernhard W. Radermacher
#
#  This program is free software: you can redistribute it and/or modify it under
#  the terms of the GNU Lesser General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
#  details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

import inspect
import threading

from hakisto import Logger

logger = Logger("imuthes")
Logger.register_excluded_source_file(inspect.currentframe().f_code.co_filename)


class Singleton:
    """Thread safe singleton class.

    Just add as a super-class.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                logger.debug(f"Creating Singleton »{cls.__name__}«.")
                cls._instance = super(Singleton, cls).__new__(cls)
            else:
                logger.debug(f"Using Singleton »{cls.__name__}«.")
        return cls._instance
