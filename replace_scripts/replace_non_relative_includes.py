from replace_expression import main


def replace_non_relative_includes(line, file_dir, iteration):
    import os

    # replace headers
    if line.startswith('#include "') or line.startswith("#include <"):
        # skip precompiled header files ...
        if (
            "precompiled.h" in line.lower()
            or "stdafx.h" in line.lower()
            or "Api.h" in line
        ):
            return line

        parent_dir = os.path.abspath(os.path.join(file_dir, os.pardir))
        grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
        
        comment = ""
        header = line.replace("#include ", "")
        idx1 = header.find('"')
        idx1 = 10000 if idx1 < 0 else idx1
        idx2 = header.find("<")
        idx2 = 10000 if idx2 < 0 else idx2
        if idx1 < idx2:
            header = header[idx1 + 1 :]
            idx1e = header.find('"')
            comment = header[idx1e + 1 :]
            header = header[:idx1e]
        else:
            idx2e = header.find(">")
            comment = header[idx2e + 1 :]
            header = header[idx2 + 1 : idx2e]
        header = header.replace("//", "/")
        while header.startswith("../"):
            header = header[3:]

        if "/" in header:
            if header.split("/", 1)[0].lower() == os.path.split(parent_dir)[1].lower():
                # the file is inside the same directory
                header = header.split("/", 1)[1]

        if os.path.exists(os.path.join(file_dir, header)):
            line = '#include "%s"' % header
        elif os.path.exists(os.path.join(parent_dir, header)):
            line = '#include "../%s"' % header
        elif os.path.exists(os.path.join(grandparent_dir, header)):
            line = '#include "../../%s"' % header
        else:
            line = "#include <%s>" % header
        if comment:
            line = line + comment.rstrip()
    return line


def replace_duplicate_includes(lines, file_path):
    new_lines = []
    count = {}
    for line in lines:
        if line.startswith("#include "):
            key = line.replace("#include ", "")

            if key in count:
                print(line + " -> " + "removed (duplicate)")
            else:
                count[key] = 1
                new_lines.append(line)
        else:
            new_lines.append(line)
    return new_lines, len(new_lines) != len(lines)


if __name__ == "__main__":

    # assert False, "This code is untested"
    main(
        replace_non_relative_includes,
        replace_callback_all_lines=replace_duplicate_includes,
    )
