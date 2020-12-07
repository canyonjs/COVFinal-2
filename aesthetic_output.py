# Creates ASCII heading
def generate_hzrule(num):
  line_break = ""
  line_break_char = "-"
  for i in range(num):
    line_break = line_break + line_break_char
  return line_break


def generate_header():
  ascii_art = open("assets/ascii_header.txt", "r")
  print(generate_hzrule(85))
  print(ascii_art.read())
  print(generate_hzrule(85))