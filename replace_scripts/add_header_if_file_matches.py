from replace_expression import main


def add_if(lines, file_path):
    found = False
    for line in lines:
        if "<boost/test/unit_test.hpp>" in line:
            found = True

    if found == False:
        if lines[0].strip() != "":
            lines.insert(0, "")
        lines.insert(0, "#include <boost/test/unit_test.hpp>")
    return lines, found == False


if __name__ == "__main__":

    main(replace_callback=None, replace_callback_all_lines=add_if, num_iterations=1)
