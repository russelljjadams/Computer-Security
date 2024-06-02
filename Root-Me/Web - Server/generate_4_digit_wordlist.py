def generate_4_digit_wordlist(filename="4-digit-wordlist.txt"):
  """Generates a wordlist of all 4-digit numbers (0000-9999) and saves it to a file.

  Args:
    filename: The name of the file to save the wordlist to. 
  """

  with open(filename, "w") as f:
    for i in range(10000):  # Loop from 0 to 9999
      f.write(f"{i:04}\n")  # Format the number with leading zeros

# Generate the wordlist
generate_4_digit_wordlist() 
print("Wordlist generated successfully!")
