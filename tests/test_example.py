import shutil

import pytest
import os
from pathlib import Path

from adapt_object_mesh_wrapper import parser, main


EXAMPLE_FILE = Path('./white_matter_mask.obj')

if os.getenv('MNI_DATAPATH'):
    data_path, *_ = os.getenv('MNI_DATAPATH').split(':')
    EXAMPLE_FILE = Path(data_path) / 'surface-extraction' / 'white_matter_mask.obj'


@pytest.mark.skipif(not EXAMPLE_FILE.is_file(), reason='No file to use as example, MNI_DATAPATH is probably undefined')
def test_main(tmp_path: Path):
    # setup example data
    inputdir = tmp_path / 'incoming'
    outputdir = tmp_path / 'outgoing'
    inputdir.mkdir()
    outputdir.mkdir()
    shutil.copy(EXAMPLE_FILE, inputdir / 'white_matter_mask.obj')

    args = ['--target-points', '1', '--iterations', '50', '--adapt', '1', '--adapt-smooth', '1']
    options = parser.parse_args(args)
    main(options, inputdir, outputdir)

    assert (outputdir / 'white_matter_mask.obj').is_file()
    assert (outputdir / 'white_matter_mask.obj.adapt_object_mesh.log').is_file()
