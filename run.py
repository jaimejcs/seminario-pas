"""Inicia API e frontend em processos separados; Ctrl+C encerra ambos."""
import subprocess
import sys
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parent
processes = []
try:
    processes.append(subprocess.Popen([sys.executable, str(ROOT / 'server.py')], cwd=ROOT))
    processes.append(subprocess.Popen([sys.executable, '-m', 'http.server', '3000', '--bind', '127.0.0.1', '--directory', str(ROOT / 'multitiers/frontend')]))
    print('\nFluxo → http://localhost:3000\nAPI → http://localhost:8000\nCtrl+C para encerrar.\n', flush=True)
    while all(p.poll() is None for p in processes):
        time.sleep(.5)
except KeyboardInterrupt:
    pass
finally:
    for process in processes:
        if process.poll() is None:
            process.terminate()
    for process in processes:
        process.wait()
