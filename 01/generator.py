import io


def generator(file: str, match_words: list[str], stop_words: list[str]):

    if not isinstance(match_words, list):
        raise TypeError("list_words must be a list of strings.")

    if not all(isinstance(word, str) for word in match_words):
        raise TypeError("list_words must be a list of strings.")

    if not isinstance(stop_words, list):
        raise TypeError("stop_words must be a list of strings.")

    if not all(isinstance(stop_word, str) for stop_word in stop_words):
        raise TypeError("stop_words must be a list of strings.")

    match_words = {word.lower() for word in match_words}
    stop_words = {word.lower() for word in stop_words}

    def process(file_obj):
        for row in file_obj:
            stripped_row = row.strip()
            formatted_row_words = stripped_row.lower().split()

            is_match = any(
                word in formatted_row_words for word in match_words
            )
            is_ignore = any(
                stop_word in formatted_row_words for stop_word in stop_words
            )

            if is_match and not is_ignore:
                yield stripped_row

    if isinstance(file, str):
        with open(file, "r", encoding="utf-8") as file_obj:
            yield from process(file_obj)
    elif isinstance(file, io.IOBase):
        yield from process(file)
    else:
        raise TypeError(f"Unsupported file type {type(file).__name__}")
