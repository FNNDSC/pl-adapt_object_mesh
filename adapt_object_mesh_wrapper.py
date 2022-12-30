#!/usr/bin/env python
import os
from concurrent.futures import ThreadPoolExecutor
import itertools
from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
import subprocess as sp

from loguru import logger

from chris_plugin import chris_plugin, PathMapper

__version__ = '1.0.0'

DISPLAY_TITLE = r"""
       _                 _             _          _     _           _                         _     
      | |               | |           | |        | |   (_)         | |                       | |    
 _ __ | |______ __ _  __| | __ _ _ __ | |_   ___ | |__  _  ___  ___| |_   _ __ ___   ___  ___| |__  
| '_ \| |______/ _` |/ _` |/ _` | '_ \| __| / _ \| '_ \| |/ _ \/ __| __| | '_ ` _ \ / _ \/ __| '_ \ 
| |_) | |     | (_| | (_| | (_| | |_) | |_ | (_) | |_) | |  __/ (__| |_  | | | | | |  __/\__ \ | | |
| .__/|_|      \__,_|\__,_|\__,_| .__/ \__| \___/|_.__/| |\___|\___|\__| |_| |_| |_|\___||___/_| |_|
| |                             | |     ______        _/ |           ______                         
|_|                             |_|    |______|      |__/           |______|                        
"""


parser = ArgumentParser(description='A ChRIS plugin wrapper for adapt_object_mesh',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-t', '--target-points', type=int, default=0,
                    help='target number of points')
parser.add_argument('-i', '--iterations', type=int, default=0,
                    help='number of post-adaptation smoothing iterations')
parser.add_argument('-a', '--adapt', type=int, default=0,
                    help='number of global adaptation iterations')
parser.add_argument('-s', '--adapt-smooth', type=int, default=0,
                    help='number of smoothing iterations per adaptation iteration')
parser.add_argument('-p', '--pattern', default='**/*.obj',
                    help='pattern for file names to include')
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')


def adapt_object_mesh(input_file: Path, output_file: Path, *args):
    cmd = ('adapt_object_mesh', input_file, output_file, *map(str, args))
    log_file = output_file.with_suffix(output_file.suffix + '.adapt_object_mesh.log')
    logger.info('{} > {}', ' '.join(map(str, cmd)), log_file)
    with log_file.open('wb') as f:
        sp.run(cmd, stdout=f, stderr=f)


@chris_plugin(
    parser=parser,
    title='adapt_object_mesh',
    category='Surfaces',         # ref. https://chrisstore.co/plugins
    min_memory_limit='200Mi',    # supported units: Mi, Gi
    min_cpu_limit='1000m',       # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0              # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    print(DISPLAY_TITLE, flush=True)

    mapper = PathMapper.file_mapper(inputdir, outputdir, glob=options.pattern)
    input_files, output_files = zip(*mapper)
    with ThreadPoolExecutor(max_workers=len(os.sched_getaffinity(0))) as pool:
        results = pool.map(
            adapt_object_mesh,
            input_files,
            output_files,
            itertools.repeat(options.target_points),
            itertools.repeat(options.iterations),
            itertools.repeat(options.adapt),
            itertools.repeat(options.adapt_smooth)
        )

    for _ in results:
        pass


if __name__ == '__main__':
    main()
