import re


def read_transcript(file_path: str = "sales_call_transcript.txt", remove_timestamp: bool = True) -> str:
    """
    @param file_path: str, path to the file
    @param remove_timestamp: bool, remove the timestamp and company name from the transcript
    @return transcript: str, the transcript
    """
    transcript = ""
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip().split(" ")

            if remove_timestamp:
                line = line[1:]  # remove timestamp
            line = " ".join(line)

            if remove_timestamp:
                line = re.sub(r'\([^()]*\)', '', line)

            line = line.replace("  ", " ").replace("  ", " ")  # repeat to handle edge case of 3 spaces
            line = line.replace("..", ".").replace("..", ".")
            line = line.replace(" :", ":")
            transcript += line + "\n"
    return transcript
