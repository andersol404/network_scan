# ============================================================
# Repository: network_scan
# Project: TCP Network Scanner
# Author: 0xander
# Watermark: created and maintained by 0xander
# Description: Lightweight networking scanner for testing open ports.
# Notes: Portuguese + English comments for traceability and style.
# ============================================================

import argparse
import socket
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

try:
    import pystyle  # type: ignore
except ImportError:  # pragma: no cover - fallback for minimal environments
    class _PystyleFallback:
        class Colors:
            rainbow = ""

        class Colorate:
            @staticmethod
            def Horizontal(color, text):
                return text

    pystyle = _PystyleFallback()


BANNER = r"""
    __  __            _   _            _
   / / / /___  ____ _| |_| |__   ___  | |_ ___  _ __
  / /_/ / __ \/ __ `/ __| '_ \ / _ \ | __/ _ \| '_ \
 / __  / /_/ / /_/ / |_| | | |  __/ | || (_) | | | |
 \/ /_/\____/\__,_/\__|_| |_|\___|  \__|\___/|_| |_|

                   made by 0xander | network scanner
"""


def print_banner() -> None:
    # Banner de apresentação; mantém o estilo visual do projeto.
    # Presentation banner; preserves the visual identity of the project.
    print(pystyle.Colorate.Horizontal(pystyle.Colors.rainbow, BANNER))


def parse_ports(port_arg: str) -> list[int]:
    # Converte a string de portas em uma lista limpa e ordenada.
    # Converts the port string into a clean and sorted list.
    ports: list[int] = []

    for item in port_arg.split(","):
        item = item.strip()
        if not item:
            continue

        if "-" in item:
            try:
                start_str, end_str = item.split("-", 1)
                start = int(start_str)
                end = int(end_str)
                if start > end:
                    start, end = end, start
                ports.extend(range(start, end + 1))
            except ValueError as exc:
                raise ValueError(f"Faixa de portas inválida: '{item}'. Use formato como '1-100' ou '80,443'.") from exc
        else:
            try:
                ports.append(int(item))
            except ValueError as exc:
                raise ValueError(f"Porta inválida: '{item}'.") from exc

    if not ports:
        raise ValueError("Nenhuma porta válida foi informada.")

    return sorted(set(ports))


def scan_port(ip: str, port: int, timeout: float = 0.5) -> tuple[int, str] | None:
    # Testa uma porta individual em modo TCP.
    # Checks one TCP port and returns service metadata if open.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        result = sock.connect_ex((ip, port))
        if result == 0:
            try:
                service = socket.getservbyport(port, "tcp")
            except OSError:
                service = "unknown"
            return port, service
    except (socket.timeout, OSError):
        return None
    finally:
        sock.close()

    return None


def resolve_target(target: str) -> str:
    # Resolve hostname para IP, mantendo compatibilidade com alvo direto.
    # Resolves hostname to IP while keeping direct target support.
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        return target


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scanner TCP simples e profissional para verificar portas abertas em um host.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("target", help="IP ou hostname para testar")
    parser.add_argument("-p", "--ports", default="1-1024", help="Portas para testar. Ex.: '1-1000' ou '80,443,8080-8090'")
    parser.add_argument("-t", "--timeout", type=float, default=0.5, help="Tempo limite por conexão em segundos")
    parser.add_argument("-w", "--workers", type=int, default=50, help="Número de threads para o scan")
    args = parser.parse_args()

    print_banner()

    try:
        ports = parse_ports(args.ports)
    except ValueError as exc:
        parser.error(str(exc))

    target = resolve_target(args.target)
    start_time = datetime.now()

    print(f"[*] Alvo: {args.target} -> {target}")
    print(f"[*] Portas: {ports[0]}-{ports[-1]} ({len(ports)} portas)")
    print(f"[*] Timeout: {args.timeout}s | Threads: {args.workers}")
    print(f"[*] Iniciando scan em {start_time.strftime('%d/%m/%Y %H:%M:%S')}\n")

    open_ports: list[tuple[int, str]] = []

    with ThreadPoolExecutor(max_workers=max(1, min(args.workers, 200))) as executor:
        futures = [executor.submit(scan_port, target, port, args.timeout) for port in ports]
        for future in futures:
            result = future.result()
            if result is not None:
                open_ports.append(result)

    open_ports.sort(key=lambda item: item[0])

    print("\n[+] Resultados")
    if not open_ports:
        print("[-] Nenhuma porta aberta foi encontrada.")
        return

    for port, service in open_ports:
        print(f"[+] {port}/tcp aberto - {service}")

    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    print(f"\n[*] Scan concluído em {elapsed:.2f}s | portas abertas: {len(open_ports)}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[-] Varredura interrompida pelo usuário.")
        sys.exit(1)
