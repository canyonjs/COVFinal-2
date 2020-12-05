# Creates ASCII heading
def head_linebreak():
  line_break = ""
  line_break_char = "-"
  for i in range(85):
    line_break = line_break + line_break_char
  return line_break


def generate_header():
  ascii_art = open("ascii_header.txt", "r")
  print(head_linebreak())
  print(ascii_art.read())
  print(head_linebreak())