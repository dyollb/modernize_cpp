from replace_expression import main


def replace_typedef_with_using(line, file_dir, iteration):
    suffix = ""
    if line.rstrip().endswith("\\") and ";" in line:
        parts = line.rsplit(";", 1)
        line = parts[0] + ";"
        suffix = parts[-1]
    # only single line expressions are replaced, excluding anything with '(' brackets
    if (
        line.lstrip().startswith("typedef")
        and line.endswith(";")
        and line.count("(") <= 1
        and not "enum" in line
        and not "struct" in line
        # and not ("," in line and not "<" in line)
    ):
        indent = line[0 : line.find("typedef")]
        line = line.replace("\t", " ")
        line = " ".join(line.split(" "))
        alias = line.rsplit(" ", 1)[1][:-1]
        line = line.replace(alias + ";", "").strip() + ";"
        line = line.replace("typedef", "%susing %s =" % (indent, alias))
    return line + suffix


if __name__ == "__main__":

    main(replace_typedef_with_using)
