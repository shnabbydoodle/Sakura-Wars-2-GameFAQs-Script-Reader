import keyboard
import sys
import time

current_line = 1

def read_paragraphs(filename, start_line=1):
    """Reads a text file and yields paragraphs one at a time, starting from a specific line."""
    global current_line
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        current_line = max(start_line - 1, 0)  # Adjust index because lines are 0-based

    # the inside of this loop or something needs to update currentline based on the slash function inside of display_and_wait
    # 4 hours later and i've decided to just use a global variable
    while current_line < len(lines):
        
        paragraph = ''
        start_line_of_paragraph = current_line
        for i in range(current_line, len(lines)):
            if lines[i].strip() == '':
                break
            paragraph += lines[i]
        current_line = i + 1

        if paragraph:
            
            #print(start_line)
            yield paragraph, start_line_of_paragraph, current_line

def save_line(line_number, filename):
    """Saves the given line number to the 'lines.txt' file, overwriting existing content."""
    with open("lines.txt", 'w', encoding='utf-8') as file:
        file.write(str(line_number) + '\n')

def display_and_wait(paragraph, start_line_of_paragraph, lines):
    """Displays a paragraph and waits for user input."""
    global current_line
    print("\n\n\n\n\n" + paragraph)
    time.sleep(0.4)

    previous_start_line = start_line_of_paragraph  # Initialize with the first paragraph's start line

    while True:
        key = keyboard.read_key()
        if key.lower() == 'n':
            return
        elif key.lower() == ',':
            save_line(previous_start_line, "lines.txt")
            print(f"Current line: {current_line}")
            time.sleep(0.4)
        elif key.lower() == '/':
            # Search for "End Prompt" from the current line
            for i in range(current_line, len(lines)):
                if "End Prompt" in lines[i]:
                    current_line = i
                    break
            print(f"Jumped to line containing 'End Prompt'")
            time.sleep(0.4)
            #print(current_line, " new current line")
            return 

        # Update the previous start line only if the current line is the end of the paragraph
        if current_line == start_line_of_paragraph + len(paragraph.splitlines()) - 1:
            previous_start_line = start_line_of_paragraph

def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: python script.py filename [line_number]")
        sys.exit(1)

    filename = sys.argv[1]
    start_line_arg = sys.argv[2] if len(sys.argv) == 3 else None

    # Attempt to read the starting line from lines.txt only if no command-line argument is provided
    if not start_line_arg:
        try:
            with open("lines.txt", 'r') as f:
                start_line_from_file = int(f.read().strip())
                start_line = start_line_from_file
        except FileNotFoundError:
            # If lines.txt doesn't exist or has invalid content, use the default
            start_line = 1
    else:
        start_line = int(start_line_arg)

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for paragraph, start_line_of_paragraph, current_line in read_paragraphs(filename, start_line):
        start_line = display_and_wait(paragraph, start_line_of_paragraph, lines)

if __name__ == '__main__':
    main()