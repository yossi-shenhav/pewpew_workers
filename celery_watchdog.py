import os
import signal
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = self.start_process()

    def start_process(self):
        return subprocess.Popen(self.command, shell=True)

    def restart_process(self):
        self.process.terminate()
        self.process.wait()
        self.process = self.start_process()

    def on_any_event(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.py'):
            print(f'{event.src_path} changed; restarting process...')
            self.restart_process()

if __name__ == "__main__":
    command = 'celery -A tasks worker --loglevel=info'
    event_handler = ChangeHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    print('Watching for file changes...')
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
