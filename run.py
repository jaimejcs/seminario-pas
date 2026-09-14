"""Inicia API e frontend; verifica portas e encerra somente seus subprocessos."""
import argparse
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--frontend-port', type=int, default=3000)
    parser.add_argument('--api-port', type=int, default=8000)
    args = parser.parse_args()
    ports = [args.frontend_port, args.api_port]
    if len(set(ports)) != 2 or any(not 1 <= port <= 65535 for port in ports):
        parser.error('Use duas portas distintas entre 1 e 65535.')
    for port in ports:
        try:
            with socket.socket() as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind(('127.0.0.1', port))
        except OSError as error:
            print(f'Não foi possível iniciar: porta {port} indisponível ({error.strerror}).', file=sys.stderr)
            print('Se o Fluxo já estiver aberto, use a execução existente. Caso contrário, encerre-a com Ctrl+C ou escolha outras portas:\n  python3 run.py --frontend-port 3001 --api-port 8001', file=sys.stderr)
            return 1
    processes = []
    try:
        processes.append(subprocess.Popen([sys.executable, str(ROOT / 'server.py'), '--port', str(args.api_port)], cwd=ROOT))
        processes.append(subprocess.Popen([sys.executable, '-m', 'http.server', str(args.frontend_port), '--bind', '127.0.0.1', '--directory', str(ROOT / 'multitiers/frontend')]))
        pending = {f'http://127.0.0.1:{args.api_port}/api/roads', f'http://127.0.0.1:{args.frontend_port}/'}
        deadline = time.monotonic() + 10
        while pending:
            if any(p.poll() is not None for p in processes) or time.monotonic() > deadline:
                print('Falha ao iniciar os servidores. Confira as mensagens acima.', file=sys.stderr)
                return 1
            for url in list(pending):
                try:
                    with urlopen(url, timeout=.3) as response:
                        if response.status == 200:
                            pending.remove(url)
                except OSError:
                    pass
            if pending:
                time.sleep(.1)
        query = f'?api=http://localhost:{args.api_port}' if args.api_port != 8000 else ''
        print(f'\nFluxo → http://localhost:{args.frontend_port}/{query}\nAPI → http://localhost:{args.api_port}\nCtrl+C para encerrar.\n', flush=True)
        while all(p.poll() is None for p in processes):
            time.sleep(.3)
        print('Um servidor encerrou inesperadamente; encerrando a execução.', file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 0
    finally:
        for process in processes:
            if process.poll() is None:
                process.terminate()
        for process in processes:
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()

if __name__ == '__main__':
    sys.exit(main())
