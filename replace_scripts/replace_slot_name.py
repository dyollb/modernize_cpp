from replace_expression import main
import re, os

def camel_case_split(identifier):
    #return re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', identifier)).split()
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]

def to_camel_case(name):
    words = []
    for word in camel_case_split(name):
        words.extend(word.split("_"))
    return "".join([w.capitalize() for w in words])

def replace_slot_name(line, validate):
    if (
        line.count("SLOT(") == 1
        and line.count(")") > 1
        and line.count("(") > 1
    ):
        parts = line.split("SLOT(")
        if len(parts) != 2:
            return line
        parts2 = parts[1].split("(", 1)
        if len(parts2) != 2:
            return line
        new_name = to_camel_case(parts2[0])
        if validate(new_name):
            line = parts[0] + "SLOT(" + new_name + "(" + parts2[1]
    return line

def process_lines(lines, file_path):
    header_path = file_path.replace(".cpp", ".h")
    if not file_path.endswith(".cpp") or not os.path.exists(header_path):
        return lines, False
    
    header_text = ""
    with open(header_path, "r") as f:
        header_text = f.read()

    changed = False
    new_lines = []
    for line in lines:
        line2 = replace_slot_name(line, lambda x: x in header_text)
        if line != line2:
            changed = True
            print("\t" + line + " -> " + line2)
        new_lines.append(line2)
    return new_lines, changed

if __name__ == "__main__":

    main(replace_callback=None, replace_callback_all_lines=process_lines)

    #print(to_camel_case("smooth_tissues_pushed"))
    #print(to_camel_case("smoothTissues_pushed"))
    #print(to_camel_case("smoothTissuesPushed"))
    #print(to_camel_case("SmoothTissuesPushed"))
    #print(to_camel_case("smoothTissuesPushed23"))
