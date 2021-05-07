from replace_expression import main


def replace_lexical_cast(line, file_dir, iteration):
    if iteration == 0:
        if "lexical_cast" in line and ("std::string" in line or "std::wstring" in line):
            line = line.replace("< ", "<").replace(" >", ">")
            line = line.replace("lexical_cast<std::string>", "std::to_string")
            line = line.replace("lexical_cast<std::wstring>", "std::to_wstring")
            line = line.replace("boost::std", "std")
    else:
        if "boost/lexical_cast.hpp" in line:
            return None
        if "using boost::lexical_cast;" in line:
            return None
        if "lexical_cast<" in line:
            raise Exception(
                "won't remove header boost/lexical_cast.hpp. it seems to be used."
            )
    return line


if __name__ == "__main__":

    main(replace_lexical_cast, num_iterations=2)
