import sys
from replace_expression import main


def replace_boost_random(line, file_dir, iteration):
    line = line.replace("boost::random::", "std::")
    if "boost::variate_generator<" in line:
        var, right = line.split("(", 1)
        index_width = var.count("\t")
        _, var = var.rsplit(" ", 1)
        expr, _ = right.split(")", 1)
        gen, dist = expr.split(",")
        line = "\t" * index_width + (
            "auto {0} = [&{1}, &{2}](){{ return {1}({2}); }};".format(
                var.strip(), dist.strip(), gen.strip()
            )
        )
    line = line.replace("boost::uniform_real", "std::uniform_real")
    line = line.replace(
        "boost::uniform_01<boost::mt19937, double>",
        "std::uniform_real_distribution<double>",
    )
    line = line.replace("boost::uniform_int", "std::uniform_int")
    line = line.replace("boost::normal_distribution", "std::normal_distribution")
    line = line.replace("bernoulli_distribution<double>", "bernoulli_distribution")
    line = line.replace("boost::mt19937", "std::mt19937")
    return line


def replace_duplicate_includes(lines, file_path):
    new_lines = []
    count = 0
    for line in lines:
        if "include <boost/random" in line:
            if count == 0:
                new_lines.append("#include <random>")
            else:
                print(line + " -> " + "removed (duplicate)")
            count += 1
        else:
            new_lines.append(line)
    return new_lines, count > 1


if __name__ == "__main__":

    # assert False, "This code is untested"
    main(replace_boost_random, replace_callback_all_lines=replace_duplicate_includes)
