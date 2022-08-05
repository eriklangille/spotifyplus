import random
import string

def random_string(length: int) -> str:
  letters = string.ascii_letters
  output = ""

  for _ in range(length):
    output += letters[random.randint(0, len(letters)-1)]

  return output


