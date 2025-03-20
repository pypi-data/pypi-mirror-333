# coding:utf-8

import os
from typing import List
from typing import Optional
from typing import Sequence

from xkits import add_command
from xkits import argp
from xkits import commands
from xkits import run_command

from xlc import Message
from xlc import Segment
from xlc.attribute import __urlhome__
from xlc.attribute import __version__


@add_command("xlc-generate", description="Generate xlc files.")
def add_cmd(_arg: argp):
    _arg.add_argument("--base", dest="directory", type=str, help="directory",
                      metavar="DIR", default="locale")
    _arg.add_argument(dest="languages", type=str, help="language", nargs="*",
                      metavar="LANG", default=["en", "zh-Hans", "zh-Hant"])


@run_command(add_cmd)
def run_cmd(cmds: commands) -> int:
    directory: str = cmds.args.directory
    languages: List[str] = cmds.args.languages
    os.makedirs(directory, exist_ok=True)
    message: Message = Message.load(directory)
    for language in languages:
        if language not in message:
            segment: Segment = Segment.generate(language)
            message.append(segment)
    for language in message:
        segment: Segment = message[language]
        filename: str = f"{segment.lang.tag.name}.xlc"
        segment.dumpf(os.path.join(directory, filename))
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = commands()
    cmds.version = __version__
    return cmds.run(root=add_cmd, argv=argv, epilog=f"For more, please visit {__urlhome__}.")  # noqa:E501
