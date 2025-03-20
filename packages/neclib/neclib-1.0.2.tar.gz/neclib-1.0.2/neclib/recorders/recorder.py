import os
import time
from datetime import datetime
from pathlib import Path
from threading import Event, Thread
from typing import List, Optional, Union

from ..core import get_logger
from .writer_base import Writer


class Recorder:
    """Data recorder, to be used with arbitrary writers.

    Parameters
    ----------
    record_root
        Root directory of data storage. All the data will be stored inside this
        directory. Subdirectories will be structured by attached writers.

    Examples
    --------
    >>> recorder = neclib.recorders.Recorder("/home/user/data")
    >>> recorder.add_writer(neclib.recorders.DBWriter(), neclib.recorders.FileWriter())
    >>> recorder.start_recording()
    >>> recorder.append("test", 1)  # Arbitrary number and type of data can be passed
    >>> recorder.stop_recording()

    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, record_root: Path) -> None:
        self.__writers: List[Writer] = []
        self.record_root = Path(record_root)
        self.recording_path = None

        self.logger = get_logger(self.__class__.__name__)

        self._thread: Optional[Thread] = None
        self._event: Optional[Event] = None

    def add_writer(self, *writers: Writer) -> None:
        """Attach writer(s) to this recorder."""
        if any(type(w) is type for w in writers):
            raise TypeError("Writer should be instantiated.")
        self.__writers.extend(writers)

    @property
    def writers(self):
        """List of attached writers."""
        return self.__writers

    def drop_writer(self, *writers: Union[int, Writer]) -> None:
        """Drop writer(s) from this recorder."""
        for writer in writers:
            if isinstance(writer, int):
                to_remove = self.__writers.pop(writer)
                to_remove.stop_recording()
            else:
                writer.stop_recording()
                self.__writers.remove(writer)

    def start_recording(
        self, record_dir: Optional[os.PathLike] = None, *, noreset: bool = False
    ) -> None:
        """Activate all attached writers."""
        if self.is_recording:
            return
        if record_dir is not None:
            if (self._thread is not None) or (self._event is not None):
                raise RuntimeError(
                    "Cannot start named recording with background check running. "
                    "Please stop the recorder first."
                )
            self.recording_path = self.record_root / Path(record_dir)
        else:
            self.recording_path = self._auto_generate_record_dir()

            if not noreset:
                self._thread = Thread(target=self._check_db_date, daemon=True)
                self._event = Event()
                self._thread.start()

        for writer in self.__writers:
            writer.start_recording(self.recording_path)

    def append(self, *args, **kwargs) -> None:
        """Pass data to all attached writers."""
        if self.recording_path is None:
            raise RuntimeError("Recorder not started. Incoming data won't be kept.")
        handled = [writer.append(*args, **kwargs) for writer in self.__writers]
        if not any(handled):
            err_msg = f"No writer handled the data: {args, kwargs}"
            self.logger.warning(err_msg[slice(0, min(100, len(err_msg)))])

    def stop_recording(self, *, noreset: bool = False) -> None:
        """Deactivate all attached writers."""
        if not self.is_recording:
            return

        if not noreset:
            if self._event is not None:
                self._event.set()
            if self._thread is not None:
                self._thread.join()
            self._thread = self._event = None

        for writer in self.__writers:
            writer.stop_recording()
        self.recording_path = None

    def _auto_generate_record_dir(self) -> Path:
        now = datetime.utcnow()
        record_dir = self.record_root / now.strftime("%Y%m") / now.strftime("%Y%m%d")
        record_dir.mkdir(parents=True, exist_ok=True)
        return record_dir

    def _check_db_date(self) -> None:
        if self._event is None:
            return
        while not self._event.is_set():
            if self.recording_path != self._auto_generate_record_dir():
                self.stop_recording(noreset=True)
                self.start_recording(noreset=True)
            time.sleep(1)

    @property
    def is_recording(self) -> bool:
        """Whether this recorder is accepting data or not."""
        return self.recording_path is not None
