# coding:utf-8

from typing import List
from typing import Optional
from typing import Sequence

from xkits import add_command
from xkits import argp
from xkits import commands
from xkits import run_command
from xlc_tools.attribute import __urlhome__
from xlc_tools.attribute import __version__

from xlc import LangT
from xlc import Segment


def generate(langtag: LangT):
    segment: Segment = Segment.generate(langtag)
    segment.dumpf(f"{segment.lang.tag}.xlc")


@add_command("xlc-generate", description="Generate xlc files.")
def add_cmd(_arg: argp):
    _arg.add_argument(dest="languages", type=str, help="language", nargs="*",
                      metavar="LANG", default=["en", "zh-Hans", "zh-Hant"])


@run_command(add_cmd)
def run_cmd(cmds: commands) -> int:
    languages: List[str] = cmds.args.languages
    for language in languages:
        generate(language)
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = commands()
    cmds.version = __version__
    return cmds.run(root=add_cmd, argv=argv, epilog=f"For more, please visit {__urlhome__}.")  # noqa:E501
