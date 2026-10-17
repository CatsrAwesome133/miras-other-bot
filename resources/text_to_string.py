import subprocess

path = "resources\\text_to_convert.txt"

def stringify(path):
    with open(path, "r", encoding="utf-8") as file:
        final = ""
        counter = 0
        for line in file:
            counter += 1
            current_line = str(line)
            final += line
            if counter//2 == 0:
                final += "\n"
    return final




if __name__ == '__main__':
    # Copies stringified text from import file to clipboard. Some symbols break.
    with open(path, "r", encoding="utf-8") as file:
        final = ""
        counter = 0
        for line in file:
            counter += 1
            current_line = str(line)
            final += line
            if counter//2 == 0:
                final += "\n"

        final = repr(final).replace("╖", "·")
        print(final)
        subprocess.run("clip", text=True, input=final)
