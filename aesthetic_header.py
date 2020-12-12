# Handles header and aesthetic bits
def generate_hzrule(num):
    # Generates a horizontal rule of num length
    line_break = ""
    line_break_char = "-"
    for i in range(num):
        line_break = line_break + line_break_char
    return line_break


def generate_header():
    # Loads ASCII Art Header
    ascii_art = open("assets/ascii_header.txt", "r")
    print(generate_hzrule(85))
    print(ascii_art.read())
    print(generate_hzrule(85))
