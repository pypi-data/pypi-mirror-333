import argparse
from pathlib import Path
import typing as t
import subprocess
import sys

from quickclone import DESCRIPTION, NAME, VERSION
from quickclone.compatibility import v0_4_0, v0_6_0
from quickclone.config.cache import (
    load_caches,
    dump_caches,
    get_cache_value,
    set_cache_value,
    AVAILABLE_CACHES
)
from quickclone.config.common import DEFAULTS_FOLDER, USER_CONFIG_FILE
from quickclone.config.configurator import load_user_config, init_user_config_file
from quickclone.delegation.tasks import create_clone_command
from quickclone.delegation.vcs.common import Command
from quickclone.remote import DirtyLocator, UniformResourceLocator, UrlAuthority


def program():
    sys.exit(main(sys.argv))


def create_argument_parser() -> argparse.ArgumentParser:
    app = argparse.ArgumentParser(
        prog="python3 -m quickclone",
        description=f"{NAME} v{VERSION}: {DESCRIPTION}",
        usage="%(prog)s [OPTION...] [REMOTE_URL] [DEST_PATH] [-- VCS_ARGS...]",
        epilog="""
You can pass additional command line arguments to the version control system by
adding them after '--'. For example, if you only want to clone the last commit
in a large repository like CPython (from https://github.com/python/cpython), you'd pass '--depth 1' after the
git clone subcommand:

```
    $ qkln python/cpython -- --depth 1
```
"""
    )
    app.add_argument(
        "--version",
        "-v",
        dest="show_version",
        help="display the version number and exit",
        action="store_const",
        const=True,
        default=False
    )
    app.add_argument(
        "remote_url",
        metavar="REMOTE_URL",
        nargs="?",
        type=str,
        default="",
        help="the url of the remote to be cloned"
    )
    app.add_argument(
        "dest_path",
        metavar="DEST_PATH",
        nargs="?",
        type=str,
        default="",
        help="the directory where the remote repository should be cloned to"
    )
    app.add_argument(
        "--last-clone",
        "-L",
        dest="get_last_clone",
        action="store_const",
        const=True,
        default=False,
        help="print the path to previously cloned repositories"
    )
    app.add_argument(
        "--last-clones-index",
        "-Z",
        dest="last_clones_index",
        action="store",
        default=0,
        type=int,
        help="the index of the path of the previously cloned repository, starting from 0 \
for the most recently cloned repository. If this value is set to -1, print all paths \
to previously cloned repositories"
    )
    app.add_argument(
        "--pretend",
        "-P",
        dest="pretend",
        action="store_const",
        const=True,
        default=False,
        help=(
            "if this flag is found, QuickClone will not perform any important "
            "actions that it would have if this flag is not found"
        )
    )
    app.add_argument(
        "--system",
        "-S",
        dest="vcs",
        help="which version control system to use: git, mercurial/hg"
    )
    app.add_argument(
        "--config-file",
        "-C",
        dest="config_file",
        metavar="CONFIG_FILE_PATH",
        help="override the default config file location"
    )
    app.add_argument(
        "--ignore",
        "-I",
        dest="ignore",
        metavar="CONFIG_KEY",
        action="append",
        required=False,
        default=[],
        help=(
            "what part of the config file to ignore. "
            "you can use dot-separated keys (like 'options.local.remotes_dir') or "
            "their short forms to specify which config values to ignore"
        )
    )
    app.add_argument(
        "--test",
        "-T",
        dest="tests",
        metavar="TEST",
        action="append",
        required=False,
        default=[],
        help=(
            "which tests to conduct: "
            "parse_authority, parse_full_url, parse_dirty_url, print_defaults_folder, config_file"
        )
    )
    return app


def process_args(parser: argparse.ArgumentParser, argv: t.List[str]) -> argparse.Namespace:
    try:
        vcsa_index = argv.index("--")
    except:
        vcsa_index = -1
    if vcsa_index == -1:
        namespace = parser.parse_args(argv)
        namespace.vcs_args = []
    else:
        namespace = parser.parse_args(argv[:vcsa_index])
        namespace.vcs_args = argv[vcsa_index+1:].copy()
    return namespace


def ignore_config(keys: t.List[str]) -> t.Set[str]:
    SHORT_FORMS = {
        "d": "options.local.remotes_dir",
        "s": "options.remote.force_scp"
    }
    ignored = set(keys)
    for short, long in SHORT_FORMS.items():
        if short in keys:
            ignored.add(long)
    return ignored


def do_compatibility():
    compat_status = v0_4_0.quickclone_cache_move()
    if compat_status == 1:
        print("Compatibility (v0.4.0) |> Cancelled move/copy!")
    compat_status = v0_6_0.quickclone_history_list()


def main(argv: t.List[str]) -> int:
    do_compatibility()
    load_caches(AVAILABLE_CACHES)
    app = create_argument_parser()
    args = process_args(app, argv[1:])
    if args.show_version:
        print(f"{NAME} v{VERSION}")
        return 0
    elif args.get_last_clone:
        last_clones_index = args.last_clones_index
        last_clones: t.Optional[t.List[str]] = get_cache_value("last_clones")
        if last_clones_index == -1:
            print("Previous repositories:")
            for i, p in enumerate(last_clones):
                print(f"  [{i}] {p}")
            return 0
        if last_clones is not None and 0 <= last_clones_index < len(last_clones):
            print(last_clones[last_clones_index])
            return 0
        else:
            raise ValueError(f"invalid --last-clones-index/-Z: {last_clones_index}")
    if len(args.tests) > 0:
        successes, test_count = conduct_tests(args.tests, args.remote_url)
        dump_caches(AVAILABLE_CACHES)
        if successes < test_count:
            print("Not all tests succeeded")
            return 1
        else:
            return 0
    try:
        result = normal(args)
    except Exception as e:
        raise e
    finally:
        dump_caches(AVAILABLE_CACHES)
    return result


# Call this function if quickclone is run with the normal set of clargs.
def normal(args: argparse.Namespace) -> int:
    dirty = DirtyLocator.process_dirty_url(args.remote_url)
    ignored = ignore_config(args.ignore)
    if args.config_file is None:
        init_user_config_file()
    try:
        configs = load_user_config(None if args.config_file is None else Path(args.config_file))
    except UnicodeDecodeError as ude:
        print(
            f"Detected non-UTF-8 encoding in '{USER_CONFIG_FILE}'! "
            f"Please make sure that the encoding for '{USER_CONFIG_FILE}' is UTF-8. "
            f"This is especially important for Windows users where the default encoding "
            f"is UTF-16."
        )
        return 2
    builder = configs.to_locator_builder()
    built_url = UniformResourceLocator.from_user_and_defaults(dirty, builder)
    vcs = configs.from_dotted_string("vcs.command")
    if args.vcs is not None:
        vcs = args.vcs
    clone_command = create_clone_command(
        vcs,
        configs,
        built_url,
        args.dest_path,
        args.vcs_args,
        {},
        ignored
    )
    print(f"Command> {clone_command.format_command_str()}")
    if args.pretend:
        print("pretend flag found! Not executing command.")
        return 0
    else:
        return run_command(clone_command).returncode


def run_command(command: Command) -> subprocess.CompletedProcess:
    result = command.run()
    if isinstance(result, subprocess.CompletedProcess):
        last_clones: t.List[str] = get_cache_value("last_clones")
        last_clones.insert(0, command.dest_path)
        set_cache_value("last_clones", last_clones)
        return result
    elif isinstance(result, subprocess.SubprocessError):
        raise result


def conduct_tests(tests: t.List[str], remote_url: str) -> t.Tuple[int, int]:
    success_counts: int = 0
    for test in tests:
        try:
            if test == "parse_authority":
                authority = UrlAuthority.process_authority(remote_url)
                print(authority)
                success_counts += 1
            elif test == "parse_full_url":
                url = UniformResourceLocator.process_url(remote_url)
                print(url)
                success_counts += 1
            elif test == "parse_dirty_url":
                dirty_url = DirtyLocator.process_dirty_url(remote_url)
                print(dirty_url)
                success_counts += 1
            elif test == "print_defaults_folder":
                print(DEFAULTS_FOLDER)
                success_counts += 1
            elif test == "config_file":
                success_counts += int(test_config_file())
            else:
                print(f"Unrecognised test: {test}")
        except:
            pass
    return success_counts, len(tests)


def test_config_file() -> bool:
    try:
        config = load_user_config()
        print(config)
        for key in ["options.remote.scheme"]:
            print(f"{key}: {config.from_dotted_string(key)}")
    except Exception as e:
        print(e)
        return False
    else:
        return True


if __name__ == "__main__":
    program()
