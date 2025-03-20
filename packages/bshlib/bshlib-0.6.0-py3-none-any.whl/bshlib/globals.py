from bshlib.singleton import Singleton

from pathlib import Path

class Global(metaclass=Singleton):
    _persisted: bool
    _rundir: Path

    def __init__(self):
        self._persisted = False
        self._rundir = None

    @property
    def persisted(self):
        return self._persisted

    @persisted.setter
    def persisted(self, value):
        self._persisted = value

    @property
    def rundir(self):
        if not self._persisted:
            raise RuntimeError('not yet initialized persistance')
        return self._rundir

    @rundir.setter
    def rundir(self, value):
        self._rundir = value

    def persist(self, rundir: Path = None):
        """Call in case of running task that requires a working directory in the filesystem.
        """
        if rundir is None:
            rundir = Path(input('input working directory: '))
            if not rundir.exists() or rundir.is_file():
                raise RuntimeError('')
        self._rundir = rundir
        self._persisted = True


# --- singleton ---

const = Global()
