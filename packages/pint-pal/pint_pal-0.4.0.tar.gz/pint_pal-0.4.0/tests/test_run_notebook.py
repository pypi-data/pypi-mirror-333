from os import makedirs
from os.path import dirname, join, split, splitext
from datetime import datetime
from glob import glob
import pytest
import pint_pal
from pint_pal.notebook_runner import run_template_notebook
test_dir = dirname(__file__)
base_dir = dirname(test_dir)
pint_pal.set_data_root(test_dir)

def config_files():
    config_files = (glob(join(test_dir, 'configs', 'B*.nb.yaml'))
                     + glob(join(test_dir, 'configs', 'J*.nb.yaml'))
                     + glob(join(test_dir, 'configs', 'B*.wb.yaml'))
                     + glob(join(test_dir, 'configs', 'J*.wb.yaml')))
    config_files = sorted(config_files)
    basenames = [splitext(split(filename)[1])[0] for filename in config_files]
    print(config_files)
    print(basenames)
    return [pytest.param(filename, id=basename) for filename, basename in zip(config_files, basenames)]

@pytest.fixture(scope='session', autouse=True)
def output_dir():
    output_dir = datetime.strftime(datetime.now(), 'tmp-%Y-%m-%dT%H-%M-%S')
    output_dir = join(base_dir, output_dir)
    makedirs(output_dir, exist_ok=True)
    return output_dir

@pytest.mark.parametrize('config_file', config_files())
def test_run_notebook(config_file, output_dir):
    """
    Run through the functions called in the notebook for each pulsar (excluding plotting).
    This will create a global log called test-run-notebooks.log, and a log file for each pulsar.

    To run for only one pulsar (using J1713+0747 as an example):
        `pytest tests/test_run_notebook.py::test_run_notebook[J1713+0747.nb]`
        or `pytest -k J1713+0747` (selects tests whose name contains "J1713+0747")
    To run for all pulsars in parallel (requires `pytest-xdist`):
        `pytest -n <workers> tests/test_run_notebook.py`
        <workers> is the number of worker processes to launch (e.g. 4 to use 4 CPU threads)
    """
    pint_pal.set_data_root(dirname(__file__))
    global_log = join(output_dir, f'test-run-notebook.log')
    with open(global_log, 'a') as f:
        run_template_notebook(
            'process_v1.2.ipynb',
            config_file,
            output_dir=output_dir,
            log_status_to=f,
            transformations = {
                'write_prenoise': "True",
                'write_results': "True",
                'use_existing_noise_dir': "True",
                'log_to_file': "True",
            },
        )
