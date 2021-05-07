from replace_expression import main


def replace_boost_foreach(line, file_dir, iteration):
    if "boost/foreach.hpp" in line:
        return None

    if "BOOST_REVERSE_FOREACH" in line:
        raise Exception("skipping file because BOOST_REVERSE_FOREACH was found")

    if (
        line.lstrip().startswith("BOOST_FOREACH")
        and line.count(")") == 1
        and line.count(",") == 1
        and not "#" in line
    ):
        line = line.replace("BOOST_FOREACH", "for").replace(",", ":")
    return line


if __name__ == "__main__":

    main(replace_boost_foreach)
