from replace_expression import main

def normalize_signature(signature):
    parts = signature.split(",")

    def remove_const_ref(m):
        p = m.strip()
        if p.startswith("const "):
            p = p[6:]
            if p.endswith("&"):
                p = p[:-1]
        return p.strip()

    return ",".join([remove_const_ref(p) for p in parts])

def normalize(keyword, line):
    key_split = keyword + "("
    if (
        line.count(key_split) == 1
        and line.count(")") > 1
        and line.count("(") > 1
    ):
        parts = line.split(key_split)
        if len(parts) != 2:
            return line
        parts2 = parts[1].split("(", 1)
        if len(parts2) != 2:
            return line
        name = parts2[0]
        parts3 = parts2[1].split(")",1)
        if len(parts3) != 2:
            return line
        signature = normalize_signature(parts3[0])
        line = parts[0] + key_split + name + "(" + signature + ")" + parts3[1]
    return line

def normalize_qt_signal_slot(line, file_dir, iteration):
    return normalize("SIGNAL", normalize("SLOT", line))

if __name__ == "__main__":

    main(normalize_qt_signal_slot)
