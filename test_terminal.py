import pytest
from terminal import MyTerminal
from zipfile import ZipFile
import os


@pytest.fixture
def terminal():
    fs_path = 'my_zip_test.zip'
    with ZipFile(fs_path, 'w') as zip_file:
        pass 
    t = MyTerminal(ZipFile(fs_path, 'a'), 'test_log.json')
    yield t
    t.fs.close()
    os.remove(fs_path)


def test_mv_1(terminal):
    terminal.fs.writestr('test_file.txt', 'content')
    terminal.fs.close()
    terminal.fs = ZipFile('my_zip_test.zip', 'a')
    terminal.mv(['test_file.txt', 'new_test_file.txt'])
    assert 'new_test_file.txt' in terminal.fs.namelist()
    assert 'test_file.txt' not in terminal.fs.namelist()


def test_mv_2(terminal):
    terminal.fs.writestr('dir/', '')
    terminal.fs.writestr('test_file.txt', 'content')
    terminal.fs.close()
    terminal.fs = ZipFile('my_zip_test.zip', 'a')
    terminal.mv(['test_file.txt', 'dir/'])
    terminal.fs.close()
    terminal.fs = ZipFile('my_zip_test.zip', 'r')
    assert 'dir/test_file.txt' in terminal.fs.namelist()
    assert 'test_file.txt' not in terminal.fs.namelist()


def test_mv_3(terminal):
    result = terminal.mv(['nonexistent.txt', 'dest.txt'])
    assert result == 'Source file not found'


def test_tail_1(terminal):
    content = '\n'.join([f'Line {i}' for i in range(20)])
    terminal.fs.writestr('test_file.txt', content)
    result = terminal.tail(['test_file.txt'])
    assert result == '\n'.join([f'Line {i}' for i in range(10, 20)])


def test_tail_2(terminal):
    content = '\n'.join([f'Line {i}' for i in range(20)])
    terminal.fs.writestr('test_file.txt', content)
    result = terminal.tail(['-5', 'test_file.txt'])
    assert result == '\n'.join([f'Line {i}' for i in range(15, 20)])


def test_tail_3(terminal):
    result = terminal.tail(['nonexistent.txt'])
    assert result == 'Invalid file name'


def test_du_1(terminal):
    terminal.fs.writestr('file1.txt', 'a' * 100)
    terminal.fs.writestr('file2.txt', 'b' * 200)
    result = terminal.du([])
    assert result == 'Total size: 300 bytes'


def test_du_2(terminal):
    terminal.fs.writestr('dir/file1.txt', 'a' * 100)
    terminal.fs.writestr('dir/file2.txt', 'b' * 200)
    result = terminal.du(['dir'])
    assert result == 'Total size: 300 bytes'


def test_du_3(terminal):
    result = terminal.du(['nonexistent_dir'])
    assert result == 'Invalid directory'
