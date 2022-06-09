import os
import subprocess
import sys
from pathlib import Path
from typing import List, TextIO


def run_clang_tidy(
    build_dir: Path,
    source_dir: Path,
    header_filter: str,
    clang_tidy: Path = None,
    clang_apply: Path = None,
    check: str = "modernize-use-nullptr",
    fix_errors: bool = False,
    logfile: TextIO = None,
):
    # directory containing run-clang-tidy.py script
    current_dir = Path(__file__).parent
    script = os.fspath(current_dir / "run-clang-tidy.py")

    # directory where checks are performed/applied
    assert source_dir.exists()

    args = [
        sys.executable,
        script,
        "-p",
        os.fspath(build_dir),
        f"-header-filter={header_filter}*",
    ]
    if clang_tidy:
        args.extend(["-clang-tidy-binary", os.fspath(clang_tidy)])
    if clang_apply:
        args.extend(["-clang-apply-replacements-binary", os.fspath(clang_apply)])
    args.extend(["-quiet"])
    args.extend([f"-checks=-*,{check}"])
    args.extend([os.fspath(source_dir)])
    if fix_errors:
        args.extend(["-fix-errors"])
    else:
        args.extend(["-fix"])

    if logfile:
        logfile.write(" ".join(args) + "\n")
    prog = subprocess.Popen(args, stdout=logfile, stderr=logfile, cwd=source_dir)
    prog.communicate()
    return True  # if prog.returncode == 0 else False -> cannot trust run-clang-tidy.py return code


def build_patch(build_dir: Path, logfile: TextIO = None, target: str = None):
    args = ["cmake", "--build", f"{build_dir}", "--parallel", "4"]
    if target:
        args.append(target)
    if logfile:
        logfile.write(" ".join(args) + "\n")
    prog = subprocess.Popen(args, stdout=logfile, stderr=logfile, cwd=build_dir)
    prog.communicate()
    return True if prog.returncode == 0 else False


def commit_patch(message: str, source_dir: Path, logfile: TextIO = None):
    args = ["git", "commit", "-am", message]
    if logfile:
        logfile.write(" ".join(args) + "\n")
    prog = subprocess.Popen(args, stdout=logfile, stderr=logfile, cwd=source_dir)
    prog.communicate()
    return True if prog.returncode == 0 else False


def revert_patch(source_dir: Path, logfile: TextIO = None):
    args = ["git", "reset", "--hard", "HEAD"]
    if logfile:
        logfile.write(" ".join(args) + "\n")
    prog = subprocess.Popen(args, stdout=logfile, stderr=logfile, cwd=source_dir)
    prog.communicate()
    return True if prog.returncode == 0 else False


def batch_run_clang_tidy(
    build_dir: Path,
    source_dir: Path,
    header_filter: str,
    checks: List[str],
    clang_tidy: Path = None,
    clang_apply: Path = None,
    target: str = None,
    log_dir: Path = None,
    no_commit: bool = False,
    fix_errors: bool = False,
    skip_build: bool = False,
    stop_if_compile_error: bool = False,
):

    if log_dir is None:
        log_dir = build_dir

    if not skip_build:
        with open(log_dir / "_check_initial_build.log", "w") as logfile:
            if not build_patch(build_dir, logfile=logfile):
                print("FAILED: build [initial build]")

    for check in checks:
        with open(log_dir / f"_check__{check}.log", "w") as logfile:
            print(f"Checking for '{check}'")
            if run_clang_tidy(
                build_dir=build_dir,
                source_dir=source_dir,
                header_filter=header_filter,
                clang_tidy=clang_tidy,
                clang_apply=clang_apply,
                check=check,
                fix_errors=fix_errors,
                logfile=logfile,
            ):
                print(f"  Applied fixes for '{check}'")
                if skip_build or build_patch(
                    build_dir=build_dir, target=target, logfile=logfile
                ):
                    if not skip_build:
                        print(f"  Built fixes for '{check}'")
                    if no_commit:
                        pass
                    elif commit_patch(
                        message=check, source_dir=source_dir, logfile=logfile
                    ):
                        print(f"  Committed fixes for '{check}'")
                    else:
                        print(f"->FAILED: git commit -am '{check}'")
                elif stop_if_compile_error:
                    print(f"->FAILED: build ['{check}'] -> Stopping")
                    return
                else:
                    revert_patch(source_dir=source_dir, logfile=logfile)
                    print(f"->FAILED: build ['{check}']")
            else:
                print(f"->FAILED: clang-tidy/apply '{check}'")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("")
    parser.add_argument(
        "-b",
        "-build",
        dest="build",
        help="path to build dir containing compile_commands.json",
    )
    parser.add_argument(
        "-s", "-source", dest="source", type=Path, help="path to source directory"
    )
    parser.add_argument(
        "-regex",
        dest="header_filter",
        default=".*",
        type=str,
        help="header filter regex (ERE-style)",
    )
    parser.add_argument(
        "-log-dir", dest="log_dir", type=Path, default=None, help="path log files"
    )
    parser.add_argument(
        "-c", "-checks", dest="checks", action="append", help="checks to be performed"
    )
    parser.add_argument(
        "-clang-tidy",
        dest="clang_tidy",
        type=Path,
        default=None,
        help="path to clang-tidy binary",
    )
    parser.add_argument(
        "-clang-apply",
        dest="clang_apply",
        type=Path,
        default=None,
        help="path to clang-apply-replacements binary",
    )
    parser.add_argument(
        "-fix-errors",
        dest="fix_errors",
        action="store_true",
        help="apply fix-its even if there are errors",
    )
    parser.add_argument(
        "-skip-build", dest="skip_build", action="store_true", help="skip build"
    )
    parser.add_argument(
        "-no", "-no-commit", dest="no_commit", action="store_true", help="skip commit"
    )
    parser.add_argument(
        "-stop-on-error",
        dest="stop_if_compile_error",
        action="store_true",
        help="cancel if there is an error",
    )
    args = parser.parse_args()

    checks = [
        "modernize-use-override",
        "modernize-use-bool-literals",
        "modernize-use-using",
        "modernize-deprecated-headers",
        "modernize-use-nullptr",
        "modernize-redundant-void-arg",
        "modernize-redundant-void-arg",
        "modernize-use-default-member-init",
        "performance-trivially-destructible",
    ]
    if args.checks is not None:
        checks = args.checks

    batch_run_clang_tidy(
        build_dir=args.build,
        source_dir=args.source,
        header_filter=args.header_filter,
        clang_tidy=args.clang_tidy,
        clang_apply=args.clang_apply,
        checks=checks,
        log_dir=args.log_dir,
        no_commit=args.no_commit,
        fix_errors=args.fix_errors,
        skip_build=args.skip_build,
        stop_if_compile_error=args.stop_if_compile_error,
    )
