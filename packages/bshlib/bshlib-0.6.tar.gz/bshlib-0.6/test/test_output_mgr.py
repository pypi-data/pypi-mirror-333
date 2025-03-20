from bshlib.globals import const
from bshlib.output_mgr import OutputMgr

from unittest import TestCase
from pathlib import Path
from typing import Final
from os import chdir, mkdir
from shutil import rmtree, unpack_archive

const.persist(Path('/home/bashiron/asset/bshlib_workdir'))

rundir: Final[Path] = const.rundir
test_ground: Final[Path] = rundir / 'test_ground'
asset: Final[Path] = rundir / 'asset'

def create_wd_dir(name):
    """Create a child directory of `test_ground`, intended to be used as the source or working directory for the CLI commands.

    Parameters
    -----
    name : `str`
        Name of directory.
    """
    mkdir(name)

def prepare_files(name, dst):
    """Prepare testing asset files by extracting an archive.

    Parameters
    -----
    name : `str`
        Name of archive to extract.
    dst : `str`
        Destination where to extract archive, relative to `test_ground`.
    """
    fin_dst = test_ground / dst
    unpack_archive(asset / f"{name}.tar", fin_dst, format='tar', filter='data')

class TestOutputMgr(TestCase):

    def setUp(self):
        chdir(rundir)
        mkdir(test_ground)
        chdir(test_ground)

    def tearDown(self):
        chdir(rundir)
        rmtree(test_ground)

    def test_init(self):
        # prepare dir
        create_wd_dir('init')
        # test
        mgr = OutputMgr(test_ground / 'init')
        mgr.switch('tini')
        # assert
        self.assertEqual(mgr.task, 'tini')

    def test_create_and_next_num(self):
        # prepare dir
        create_wd_dir('create-and-num')
        # test & assert
        mgr = OutputMgr(test_ground / 'create-and-num')
        mgr.switch('numtest')
        mgr.create_task_root()
        nnum = mgr.next_num()
        self.assertEqual(nnum, 0)
        mgr.create('some\ncontent\nverygoood', '.txt')
        nnum = mgr.next_num()
        self.assertEqual(nnum, 1)

    def test_rearrange(self):
        # prepare dir
        create_wd_dir('rearrange')
        # test & assert
        mgr = OutputMgr(test_ground / 'rearrange')
        mgr.switch('arr')
        mgr.create_task_root()
        Path(mgr.get_task_root() / f'{mgr.task}.txt').touch()
        Path(mgr.get_task_root() / f'{mgr.task}.md').touch()
        mgr.create('something', '.txt')
        self.assertEqual(mgr.next_num(), 1)
        mgr.rearrange()
        self.assertEqual(mgr.next_num(), 3)
