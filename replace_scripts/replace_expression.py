import os
import shutil
import fnmatch
import traceback


def replace_line_by_line(
    file_path,
    file_dir,
    replace_callback,
    num_iterations=1,
    replace_callback_all_lines=None,
    simulate=False,
):

    with open(
        file_path, "r"
    ) as fp:  # encoding="ascii", errors="surrogateescape") as fp:
        lines = fp.read().splitlines()

    new_lines = lines
    found = False

    if replace_callback:
        for iteration in range(num_iterations):
            new_lines = []
            for line_orig in lines:
                line = line_orig.rstrip()

                # process line
                line = replace_callback(line, file_dir, iteration)

                # line was removed
                if line is None:
                    found = True
                    if simulate:
                        print("\t" + line_orig + " -> " + "removed")
                else:
                    # line has changed
                    if line != line_orig.rstrip():
                        found = True
                        if simulate:
                            print("\t" + line_orig + " -> " + line)
                        new_lines.append(line)
                    else:
                        new_lines.append(line_orig)

            # nothing todo
            if not found:
                return
            lines = new_lines

    if replace_callback_all_lines:
        new_lines, changed = replace_callback_all_lines(new_lines)
        if changed:
            found = True

    if not simulate and found:
        try:
            tmp_file = file_path + ".bak"
            with open(tmp_file, "w") as fp:
                for line in new_lines:
                    print(line, file=fp)
            shutil.move(tmp_file, file_path)
        except:
            print("\t" + "Skipped %s" % file_path)


def skip_file(name, exlude_patterns):
    if exlude_patterns is None:
        return False

    for pattern in exlude_patterns:
        if len(fnmatch.filter([name], pattern)) != 0 or pattern in name:
            print("[INFO] skipping %s because of pattern %s" % (name, pattern))
            return True
    return False


def listdir(path, exlude_patterns=[]):
    """
    recursively walk directory to specified depth
    :param path: (str) path to list files from
    :yields: (str) filename, including path
    """
    for filename in os.listdir(path):
        if skip_file(filename, exlude_patterns):
            continue
        yield os.path.join(path, filename)


def walk(path=".", depth=None, exlude_patterns=[], verbose=False):
    """
    recursively walk directory to specified depth
    :param path: (str) the base path to start walking from
    :param depth: (None or int) max. recursive depth, None = no limit
    :yields: (str) filename, including path
    """
    if depth and depth == 1:
        for filename in listdir(path, exlude_patterns):
            yield filename
    else:
        top_pathlen = len(path) + len(os.path.sep)
        for dirpath, dirnames, filenames in os.walk(path):

            if skip_file(dirpath, exlude_patterns):
                continue
            if verbose:
                print("[INFO] processing %s" % (dirpath))

            dirlevel = dirpath[top_pathlen:].count(os.path.sep)
            if depth and dirlevel >= depth:
                dirnames[:] = []
            else:
                for filename in filenames:
                    yield os.path.join(dirpath, filename)


def process_all_files(
    root_dir,
    replace_callback,
    num_iterations=1,
    replace_callback_all_lines=None,
    simulate=False,
    exlude_patterns=[],
    max_depth=10,
):
    def process_file(file_path):
        try:
            replace_line_by_line(
                file_path,
                os.path.dirname(file_path),
                replace_callback=replace_callback,
                num_iterations=num_iterations,
                replace_callback_all_lines=replace_callback_all_lines,
                simulate=simulate,
            )
        except UnicodeDecodeError:
            print("\n[ERROR] UnicodeDecodeError in %s:\n" % file_path)
        except Exception:
            print("[ERROR] %s:\n\n" % file_path, traceback.format_exc())

    if os.path.isfile(root_dir) and not os.path.isdir(root_dir):
        process_file(root_dir)

    for file_path in walk(
        root_dir, depth=max_depth, exlude_patterns=exlude_patterns, verbose=simulate
    ):

        if os.path.isfile(file_path):
            if (
                file_path.endswith(".cpp")
                or file_path.endswith(".cxx")
                or file_path.endswith(".h")
                or file_path.endswith(".hpp")
                or file_path.endswith(".inl")
            ):
                process_file(file_path)


def main(replace_callback, num_iterations=1, replace_callback_all_lines=None):
    import argparse

    parser = argparse.ArgumentParser("")
    parser.add_argument(
        "-source",
        dest="source",
        help="path to source directory",
    )
    parser.add_argument(
        "-simulate",
        action="store_true",
        help="only show changes without modifying files",
    )
    parser.add_argument(
        "-depth", dest="depth", default=10, help="max depth for recursion"
    )
    parser.add_argument(
        "-e",
        "-exlude-pattern",
        dest="exlude_patterns",
        action="append",
        help="pattern to exclude specific folder(s) with Unix shell-style wildcards (see fnmatch)",
    )
    args = parser.parse_args()

    process_all_files(
        args.source,
        replace_callback=replace_callback,
        num_iterations=num_iterations,
        replace_callback_all_lines=replace_callback_all_lines,
        simulate=args.simulate,
        exlude_patterns=args.exlude_patterns,
        max_depth=int(args.depth),
    )
