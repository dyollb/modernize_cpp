from replace_expression import main


def remove_newlines(lines, file_path):
    new_lines = []

    comment_started = False
    next_line = ""
    for line in lines:
        stripped = line.strip()

        # special case: /* .... */ style comments
        if not comment_started and stripped.count("/*") == 1:
            comment_started = True
        if comment_started and stripped.count("*/") == 1:
            comment_started = False

        if not comment_started and stripped and stripped[-1] in [',', '(']:
            if next_line:
                next_line += " " + stripped
            else:
                next_line = line
        else:
            if next_line:
                new_lines.append(next_line + " " + stripped)
                next_line = ""
            else:
                new_lines.append(next_line + line)

    return new_lines, len(lines)!=len(new_lines)


if __name__ == "__main__":

    # assert False, "This code is untested"
    main(replace_callback=None, replace_callback_all_lines=remove_newlines)
