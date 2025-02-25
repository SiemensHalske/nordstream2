import random
import string


def generate_chaotic_text(file_name, num_lines, line_length):
    # Define the pool of characters: letters, digits, and symbols
    chaotic_characters = string.ascii_letters + string.digits + string.punctuation

    # Open a file for writing
    with open(file_name, "w", encoding="utf-8") as file:
        for _ in range(num_lines):
            # Generate a random line of chaotic characters
            line = ''.join(random.choice(chaotic_characters)
                           for _ in range(line_length))
            file.write(line + "\n")

    print(f"Chaotic text file '{file_name}' created successfully!")


# Customize the file name, number of lines, and length of each line
file_name = "chaotic_text.txt"
num_lines = 1000  # Number of lines in the file
line_length = 100  # Length of each line

# Call the function to generate the chaotic text file
generate_chaotic_text(file_name, num_lines, line_length)
