from replace_expression import main


def replace_boost_array(line, file_dir, iteration):
    import os

    # replace headers
    if "boost/" in line:
        line = line.replace("<boost/array.hpp>", "<array>")

    # replace use in line
    if "boost::" in line:
        line = line.replace("boost::array", "std::array")
    return line


def replace_duplicate_includes(lines):
    new_lines = []
    count = 0
    for line in lines:
        if "<array>" in line:
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
    main(replace_boost_array, replace_callback_all_lines=replace_duplicate_includes)
