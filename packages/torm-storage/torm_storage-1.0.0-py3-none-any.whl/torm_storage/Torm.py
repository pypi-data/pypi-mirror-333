import pathlib

import filelock
import msgpack
import orjson
from tinydb.storages import Storage


class TormStorage(Storage):
    def __init__(self, filename="temp.db"):
        self._file = pathlib.Path(filename)
        self._lockfile = pathlib.Path(f"{self._file.parent.joinpath(self._file.stem)}.lock")
        self._lock = filelock.FileLock(self._lockfile, thread_local=False)

        if not self._file.is_file():
            self._file.parent.mkdir(exist_ok=True, parents=True)
            self._file.touch(exist_ok=True)
            self._lockfile.touch(exist_ok=True)

    def read(self):
        with self._lock:
            with open(self._file, 'r+b') as handle:
                try:
                    raw_data = msgpack.unpackb(handle.read()).decode()
                    data = orjson.loads(raw_data)
                    return data
                except Exception as _:
                    return None

    def write(self, data):
        with self._lock:
            with open(self._file, 'w+b') as handle:
                handle.write(msgpack.dumps(orjson.dumps(data)))
