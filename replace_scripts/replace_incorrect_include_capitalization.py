from replace_expression import main


def replace_incorrect_include_capitalization(line, file_dir, iteration):
    import os

    if line.lstrip().startswith('#include "'):
        header = line[line.find('"') + 1 : line.rfind('"')]
        header_path = os.path.join(file_dir, header)
        if os.path.exists(header_path):
            relpath_name = os.path.split(header)
            if len(relpath_name) == 2:
                for f in os.listdir(os.path.join(file_dir, relpath_name[0])):
                    if f.lower() == relpath_name[1].lower():
                        if f != relpath_name[1]:
                            if len(relpath_name[0]) != 0:
                                line = '#include "%s/%s"' % (relpath_name[0], f)
                            else:
                                line = '#include "%s"' % (f)
                        break
    return line


if __name__ == "__main__":

    main(replace_incorrect_include_capitalization)
