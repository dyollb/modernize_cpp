from replace_expression import main


def replace_line_if_contains_key(key, line, file_dir, iteration):
    if key in line:
        return None
    return line


if __name__ == "__main__":

    key = '#include "Some_legacy_header.h"'
    replace = lambda line, file_dir, iteration: replace_line_if_contains_key(
        key, line, file_dir, iteration
    )

    main(replace, num_iterations=1)
