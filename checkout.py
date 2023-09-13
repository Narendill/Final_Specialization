import logging
import subprocess


def checkout(cmd: str, text: str) -> bool | None:
    """Выполняет команду и в выводе ищет текст."""
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                encoding='utf-8')
    except:
        logging.exception(f'Exception while executing the command {cmd}')
        return None
    if text in result.stdout and result.returncode == 0 or text in result.stderr:
        return True
    else:
        return False
