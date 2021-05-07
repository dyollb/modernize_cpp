from replace_expression import main


def replace_empty_inheritancelist(lines):
    from rreplace import rreplace

    new_lines = []
    N = len(lines)
    stripped_lines = [l.strip() for l in lines]
    found = False

    for i in range(N):
        if (
            stripped_lines[i].endswith("() :")
            or stripped_lines[i].endswith("),")
            or stripped_lines[i] == ":"
            or stripped_lines[i] == ","
        ):
            inext = i + 1
            for i2 in range(i + 1, N):
                if not len(stripped_lines[i2]) == 0:
                    inext = i2
                    break

            if stripped_lines[inext].startswith("{"):
                if stripped_lines[i].endswith(":"):
                    line = rreplace(lines[i], ":", "", 1)
                else:
                    line = rreplace(lines[i], ",", "", 1)
                print("replacing %s with %s" % (lines[i], line))
                new_lines.append(line)
                found = True
            else:
                new_lines.append(lines[i])
        else:
            new_lines.append(lines[i])
    return new_lines, found


def remove_empty_lines(lines):
    lines, changed = replace_empty_inheritancelist(lines)
    if not changed:
        return lines, changed

    new_lines = []
    N = len(lines)

    for i in range(N):
        skip = False
        if len(lines[i].strip()) == 0:
            inext = i + 1
            for i2 in range(i + 1, N):
                if len(lines[i2].strip()) != 0:
                    inext = i2
                    break
            if inext < N and lines[inext].lstrip().startswith("{"):
                skip = True
                changed = True
        if not skip:
            new_lines.append(lines[i])
    return new_lines, changed


if __name__ == "__main__":

    # assert False, "This code is untested"
    main(replace_callback=None, replace_callback_all_lines=remove_empty_lines)
