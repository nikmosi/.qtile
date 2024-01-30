#!/usr/bin/env python
import os
import subprocess as sb

import yarl
from loguru import logger


def send_notify(title: str, body: str = ""):
    sb.check_call(["notify-send", title, body])


def main():
    window_search_command = "xdotool search --onlyvisible --class firefox"
    try:
        proc = sb.check_output(window_search_command.split(), text=True)
    except sb.CalledProcessError:
        logger.warning("can't find firefox")
        return
    out = proc.strip().split()

    send_key_command = (
        "xdotool key --window {id} --delay 20 --clearmodifiers ctrl+l ctrl+c Escape F6"
    )
    get_clip = "xclip -o -selection clipboard".split()
    for proc_id in out:
        f = send_key_command.format(id=proc_id)
        old_clip = sb.check_output(get_clip)
        sb.check_call(f.split())
        clip = sb.check_output(get_clip, text=True)
        sb.run(["xsel", "-ib"], input=old_clip)
        logger.info(clip)

        url = yarl.URL(clip)
        if not url.is_absolute():
            break
        workdir = os.path.expanduser(os.path.join("~", "Downloads"))
        if url.host == "tl.rulate.ru":
            send_notify("Load", f"from {url.path}")
            command = f"tlrulate -w {workdir} {str(url)}"
            logger.info(str(command))

            with sb.Popen(
                command, bufsize=1, stdout=sb.PIPE, shell=True, encoding="utf-8"
            ):
                pass
            send_notify(f"Saved {url.path}", f"to {workdir}")


if __name__ == "__main__":
    main()
