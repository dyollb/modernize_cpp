import sys
from replace_expression import main


def replace_boost_function(line, file_dir, iteration):
    line = line.replace("<boost/function.hpp>", "<functional>")
    line = line.replace("boost::function", "std::function")
    return line


if __name__ == "__main__":

    # assert False, "This code is untested"
    main(replace_boost_function)
