import os
import requests
from rich import print
from rich.progress import Progress, BarColumn
import time
import argparse
import threading
from datetime import datetime


class CustomBarColumn(BarColumn):
    def render(self, task):
        completed = task.completed / task.total
        bar = "━" * int(completed * 50)
        remaining = "┈" * (50 - len(bar))
        return f"[green]{bar}[white]{remaining}"


def bytes_to_human(byte_size):
    suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]
    index = 0
    while byte_size >= 1024 and index < len(suffixes) - 1:
        byte_size /= 1024
        index += 1
    return f"{byte_size:.2f} {suffixes[index]}"


def download_file(url, output_path, retries=3, timeout=60, proxies=None):
    headers = {
        'User-Agent': 'CustomDownloadScript/1.0',
    }

    # Check if the file already exists and get the partial download size if any
    file_size = 0
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(
            f"Resuming download... Already downloaded {bytes_to_human(file_size)}")

    # Prepare range header for resuming
    headers['Range'] = f"bytes={file_size}-"

    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(
                url, headers=headers, stream=True, timeout=timeout, proxies=proxies)
            total_size = int(response.headers.get(
                'Content-Length', 0)) + file_size
            with open(output_path, 'ab') as file, Progress(
                CustomBarColumn(50),
                "[progress.percentage]{task.percentage:.3}%",
                "•",
                f"[{bytes_to_human(total_size)}]",
                refresh_per_second=30,
            ) as progress:
                task = progress.add_task(
                    "[cyan]Downloading...", total=total_size)

                start_time = time.time()
                last_reported_time = start_time
                bytes_received = file_size

                for chunk in response.iter_content(chunk_size=2048):
                    file.write(chunk)
                    bytes_received += len(chunk)
                    progress.update(task, advance=len(chunk))

                    # Calculate download speed and ETA
                    if time.time() - last_reported_time > 1:
                        elapsed = time.time() - start_time
                        speed = bytes_received / elapsed
                        eta = (total_size - bytes_received) / \
                            speed if speed > 0 else 0
                        print(
                            f"Speed: {bytes_to_human(speed)}/s ETA: {int(eta)}s", end='\r')
                        last_reported_time = time.time()

            print(f"\nDownload completed: {output_path}")
            log_download_metadata(url, output_path, total_size, elapsed)
            break
        except (requests.exceptions.RequestException, KeyboardInterrupt) as e:
            attempt += 1
            print(f"[red]Error: {e}, retrying... ({attempt}/{retries})")
            time.sleep(5)
            if attempt == retries:
                print("[red]Maximum retries reached. Download failed.")
                break


def log_download_metadata(url, output_path, total_size, elapsed):
    with open("download_log.txt", "a") as log_file:
        log_file.write(
            f"{datetime.now()} | URL: {url} | File: {output_path} | Size: {bytes_to_human(total_size)} | Time: {elapsed:.2f}s\n")


def download_multiple_files(urls, output_paths, proxies=None):
    threads = []
    for url, output in zip(urls, output_paths):
        thread = threading.Thread(
            target=download_file, args=(url, output, 3, 60, proxies))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def main():
    parser = argparse.ArgumentParser(
        description="Download a file with progress bar")
    parser.add_argument("urls", nargs="+",
                        help="URLs of the files to download")
    parser.add_argument("outputs", nargs="+",
                        help="Paths to save the downloaded files")
    parser.add_argument(
        "--proxy", help="Proxy server to use, e.g., http://127.0.0.1:8080")

    args = parser.parse_args()

    # Set up proxy if provided
    proxies = None
    if args.proxy:
        proxies = {
            "http": args.proxy,
            "https": args.proxy,
        }

    if len(args.urls) == 1:
        try:
            download_file(args.urls[0], args.outputs[0], proxies=proxies)
        except KeyboardInterrupt:
            print('[on red]Keyboard interrupt.')
    else:
        download_multiple_files(args.urls, args.outputs, proxies=proxies)


if __name__ == "__main__":
    main()
