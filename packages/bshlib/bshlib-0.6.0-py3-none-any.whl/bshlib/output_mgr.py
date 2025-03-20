from bshlib.suffix_mgr import SuffixMgr, ObjId, is_suffix, extract_num, extract_name

import os
from pathlib import Path

from typing import TextIO
from os import PathLike

def extract_number(path):
    """
    Extract the sequence number from the file.

    Parameters
    -----
    path : Path
        Path of the file to extract from.

    Returns
    -----
    int
        Sequence number.
    """
    return extract_num(path.stem)

def task_op(function):
    """
    Check that `task` attribute is set.

    Can only be used to decorate `OutputMgr`'s methods since it takes an `OutputMgr` object as first argument.

    Returns
    -----
    None
    """
    def wrapper(mgr, *args, **kwargs):
        mgr.task_check()
        return function(mgr, *args, **kwargs)

    return wrapper

class OutputMgr:
    root: Path
    """Output root"""
    task: str
    """Task"""

    def __init__(self, out_root):
        """
        Parameters
        -----
        out_root : PathLike[str] or str
            Output root from where the manager will operate.
        """
        match out_root:
            case Path():
                self.root = out_root
            case os.PathLike() | str():
                self.root = Path(out_root)
            case _:
                raise TypeError
        self.task = None

    def switch(self, task):
        """
        Switch to operating on `task`.

        Parameters
        -----
        task : str
            Task.

        Returns
        -----
        None
        """
        self.task = task

    def create_root(self):
        """
        Create output root.

        Returns
        -----
        None
        """
        try:
            os.mkdir(self.root)
        except FileExistsError:
            print('directory exists. skipping..')

    @task_op
    def create_task_root(self):
        """
        Create task root.

        Returns
        -----
        None
        """
        try:
            os.mkdir(self.root / self.task)
        except FileExistsError:
            print('directory exists. skipping..')

    @task_op
    def get_task_root(self):
        """
        Get the task root.

        Returns
        -----
        Path
            Task root directory.
        """
        return self.root / self.task

    @task_op
    def mkfile(self, ext):
        """
        Creates and opens file in the task folder, in text-write mode. The file is suffixed and the provided extension is added.

        Parameters
        -----
        ext : str
            File extension. Dots included.

        Returns
        -----
        TextIO
            Open file handle.
        """
        return self.__strong_open(self.root / self.task / f"{self.task}_{self.next_num()}{ext}", 'wt')

    @task_op
    def create(self, content, ext):
        """
        Create file in the task folder. The file is suffixed and the provided extension is added. Fills the file with provided content. Writes in text mode.

        Parameters
        -----
        content : any
            Content to write to file.
        ext : str
            File extension. Dots included.

        Returns
        -----
        Path
            Path of the created file.
        """
        path = self.root / self.task / f"{self.task}_{self.next_num()}{ext}"
        with self.__strong_open(path, 'wt') as f:
            f.write(content)
        return path

    @task_op
    def clear(self):
        """
        Clear task directory.

        Returns
        -----
        None
        """
        for ch in (self.root / self.task).iterdir():
            ch.unlink()

    @task_op
    def list_task_files(self):
        """
        Return a list of all task files.

        Returns
        -----
        list[Path]
            Files.
        """
        return self.list_suffixed() + self.list_basic()

    @task_op
    def list_suffixed(self):
        """
        Return a list of task files that are suffixed.

        Returns
        -----
        list[Path]
            Suffixed files.
        """
        taskdir = self.root / self.task
        return [taskdir / path for path in taskdir.iterdir() if self.is_suffixed_from_task(path)]

    @task_op
    def list_basic(self):
        """
        Return a list of task files that are not suffixed.

        Since duplicate filenames are not allowed, the only way for this to return more than one file is if they have different extensions.

        Returns
        -----
        list[Path]
            Non-suffixed files.
        """
        taskdir = self.root / self.task
        return [taskdir / path for path in taskdir.iterdir() if self.is_basic_from_task(path)]

    @task_op
    def is_suffixed_from_task(self, path):
        """
        Returns whether `path` is from task and suffixed.

        Parameters
        -----
        path : Path
            Path to check.

        Returns
        -----
        bool
            Result.
        """
        if is_suffix(path.stem):
            return extract_name(path.stem) == self.task
        else:
            return False

    @task_op
    def is_basic_from_task(self, path):
        """
        Returns whether `path` is from task and not suffixed.

        Parameters
        -----
        path : Path
            Path to check.

        Returns
        -----
        bool
            Result.
        """
        return path.stem == self.task

    @task_op
    def rearrange(self):
        """
        Rename the task files so they follow sequential order again. Useful for gaps in the numeric naming sequence
        caused by file deletion.

        Returns
        -----
        None
        """
        files = self.list_task_files()
        ids = [f.stem for f in files]
        bundle_ls = [ObjId(file, _id) for file, _id in zip(files, ids)]
        sfm = SuffixMgr(bundle_ls)
        for f in files:
            os.rename(f, f.with_stem(sfm.get(f).id))

    @task_op
    def next_num(self):
        """
        Get next suffix number.

        Returns
        -----
        int
            Next number.
        """
        # we don't care about unsuffixed
        names = [f.stem for f in self.list_suffixed()]

        # use a dummy, we only want the number
        obj_ls = [object()]
        obj_ls *= len(names)

        bundle_ls = [ObjId(obj, _id) for obj, _id in zip(obj_ls, names)]
        num = SuffixMgr(bundle_ls).sequence_pointer(self.task)
        if num is not None:
            return num + 1
        else:
            return 0

# ----- MISC -----

    def __strong_open(self, path, mode):
        """
        Open file, creating parent directory if it doesn't exist.

        Parameters
        -----
        path : Path
            File to open.
        mode : str
            `os.open` mode.

        Returns
        -----
        ret : TextIO
            File handle.
        """
        try:
            fd = open(path, mode)
        except FileNotFoundError:
            os.mkdir(path.parent)
            # retry
            fd = self.__strong_open(path, mode)
        return fd

    def task_check(self):
        """
        Check if `task` is set. Raises error if it doesn't.

        Returns
        -----
        None
        """
        if self.task is None:
            raise UnboundLocalError('task not yet set')
