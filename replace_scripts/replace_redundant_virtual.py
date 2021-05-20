from replace_expression import main


def replace_virtual(line, file_dir, iteration):
    import os

    # replace headers
    if "virtual " in line and " override" in line:
        line = line.replace("virtual ", "")
    return line


if __name__ == "__main__":

    # assert False, "This code is untested"
    main(replace_virtual)
