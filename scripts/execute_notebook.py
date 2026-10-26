"""Ejecuta el notebook con el intérprete del entorno actual, sin instalar un kernel global."""
from pathlib import Path
import json
import os
import sys
import tempfile

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'pronostico_demanda_taxis.ipynb'

def main():
    print('Preparando kernel y lectura del notebook...', flush=True)
    for variable in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS']:
        os.environ.setdefault(variable, '1')
    notebook = nbformat.read(PATH, as_version=4)
    with tempfile.TemporaryDirectory(prefix='taxis-kernel-') as temporary:
        base = Path(temporary)
        kernel = base / 'kernels' / 'taxis-portfolio'
        kernel.mkdir(parents=True)
        (kernel / 'kernel.json').write_text(json.dumps({
            'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
            'display_name': 'Taxis', 'language': 'python',
        }), encoding='utf-8')
        previous = os.environ.get('JUPYTER_PATH')
        os.environ['JUPYTER_PATH'] = str(base) + (os.pathsep + previous if previous else '')
        try:
            def progress(cell, cell_index, **kwargs):
                if cell.cell_type == 'code':
                    print(f'Ejecutando celda {cell_index + 1}/{len(notebook.cells)}', flush=True)
            client = NotebookClient(
                notebook, timeout=1800, startup_timeout=60, kernel_name='taxis-portfolio',
                resources={'metadata': {'path': str(ROOT)}},
                allow_errors=False, on_cell_start=progress,
            )
            client.execute()
        finally:
            if previous is None: os.environ.pop('JUPYTER_PATH', None)
            else: os.environ['JUPYTER_PATH'] = previous
        # Mantiene un kernelspec portable al abrir el resultado en Jupyter.
        notebook.metadata['kernelspec'] = {
            'display_name':'Python 3 (ipykernel)', 'language':'python', 'name':'python3'
        }
        nbformat.write(notebook, PATH)
    print('Notebook completado sin errores.', flush=True)

if __name__ == '__main__':
    main()
