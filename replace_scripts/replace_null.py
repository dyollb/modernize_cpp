from replace_expression import main


def replace_null(line, file_dir, iteration):
    if (
        "freetype" in file_dir
        or "nanovg" in file_dir
        or "nanosvg" in file_dir
        or "yocto" in file_dir
    ):
        return line
    if "DWORD" in line:
        return line
    if "::SendMessage" in line:
        return line
    if "Pdh" in line:
        return line

    if "NULL" in line:
        line = line.replace("= NULL;", "= nullptr;")
        line = line.replace("=NULL;", "= nullptr;")
        line = line.replace("(NULL)", "(nullptr)")
        line = line.replace("= NULL &&", "= nullptr &&")
        line = line.replace("= NULL ||", "= nullptr ||")
        line = line.replace("= NULL )", "= nullptr )")
        line = line.replace("= NULL)", "= nullptr)")
        line = line.replace(", NULL,", ", nullptr,")
        line = line.replace(", NULL)", ", nullptr)")
    return line


if __name__ == "__main__":

    main(replace_null)
