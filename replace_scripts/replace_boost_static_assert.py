from replace_expression import main


def replace_last(line, old, new):
    idx = line.rfind(old)
    return line[:idx] + new + line[idx + len(old) :]


def replace_boost_static_assert(line, file_dir, iteration):
    # replace use in line
    line = line.replace("BOOST_STATIC_ASSERT_MSG", "static_assert")

    if "BOOST_STATIC_ASSERT(" in line and line.count(")") >= 1 and line.count(";"):
        line = line.replace("BOOST_STATIC_ASSERT", "static_assert")
        expression = line.partition("(")[2].rpartition(")")[0].strip()
        line = replace_last(line, ")", ', "Condition %s failed")' % expression)
    return line


def remove_includes(lines, file_path):
    new_lines = []
    for line in lines:
        if not "<boost/static_assert.hpp>" in line:
            new_lines.append(line)
    return new_lines, len(new_lines) != len(lines)


if __name__ == "__main__":

    # assert False, "This code is untested"
    main(replace_boost_static_assert, replace_callback_all_lines=remove_includes)
