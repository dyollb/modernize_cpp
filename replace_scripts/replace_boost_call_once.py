import sys
from replace_expression import main


def replace_boost_call_once(line, file_dir, iteration):
    line = line.replace("<boost/thread/once.hpp>", "<mutex>")
    line = line.replace(
        "boost::once_flag once_flag = BOOST_ONCE_INIT", "std::once_flag once_flag"
    )
    line = line.replace(
        "boost::once_flag flag = BOOST_ONCE_INIT", "std::once_flag flag"
    )
    line = line.replace("boost::once_flag", "std::once_flag")
    line = line.replace("boost::call_once", "std::call_once")
    return line


def replace_duplicate_includes(lines):
    new_lines = []
    count = 0
    for line in lines:
        if "include <mutex>" in line:
            if count == 0:
                new_lines.append(line)
            else:
                print(line + " -> " + "removed (duplicate)")
            count += 1
        else:
            new_lines.append(line)
    return new_lines, count > 1


if __name__ == "__main__":

    # assert False, "This code is untested"
    main(replace_boost_call_once, replace_callback_all_lines=replace_duplicate_includes)
