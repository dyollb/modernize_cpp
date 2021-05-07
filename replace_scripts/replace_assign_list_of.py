from replace_expression import main


def _test():
    test = "std::vector<DWORD> order = boost::assign::list_of(mio('X','V','I','D'))(mio('D','I','V','X'))(mio('I','Y','U','V'));"
    print("\n\n" + test)
    print(replace_assign_list_of(test, "", True))


def split_balanced(txt, initial_count):
    """ find first split where all opened brackets are closed """
    count = initial_count
    for idx, i in enumerate(txt):
        if i == "(":
            count += 1
        elif i == ")":
            count -= 1
        if count == 0:
            return txt[0:idx], txt[(idx + 1) :]
    return txt, ""


def replace_assign_list_of(line, file_dir, iteration):
    if iteration == 0:
        if line.count("assign::list_of") == 1 and line.endswith(";"):
            line = line.replace("boost::assign::list_of", "assign::list_of")
            line = line.replace("assign::list_of ", "assign::list_of")

            prefix, rest = line.split("assign::list_of(")
            rest = rest.replace(") (", ")(")
            items = rest.split(")(")
            last_item, suffix = split_balanced(items[-1], 1)
            items[-1] = last_item

            line = "%s{ %s }%s" % (prefix, ", ".join(items), suffix)
    else:

        if "boost/assign.hpp" in line:
            return None
        if "boost/assign/list_of.hpp" in line:
            return None
        if "assign::" in line:
            raise Exception(
                "won't remove header boost/assign.hpp. it seems to be used."
            )
    return line


if __name__ == "__main__":

    main(replace_assign_list_of, num_iterations=2)
