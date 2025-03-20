from .log_message import log_message

# 0_o

def info(*, text, text_color="green", letter_color="green", text_back=None, letter_back=None, text_case=None, letter_case="upper"):
    return log_message(text, "Info", text_color, letter_color, text_back, letter_back, text_case, letter_case)

def warning(*, text, text_color="yellow", letter_color="yellow", text_back=None, letter_back=None, text_case=None, letter_case="upper"):
    return log_message(text, "Warning", text_color, letter_color, text_back, letter_back, text_case, letter_case)

def error(*, text, text_color="light-red", letter_color="light-red", text_back=None, letter_back=None, text_case=None, letter_case="upper"):
    return log_message(text, "Error", text_color, letter_color, text_back, letter_back, text_case, letter_case)

def debug(*, text, text_color="cyan", letter_color="cyan", text_back=None, letter_back=None, text_case=None, letter_case="upper"):
    return log_message(text, "Debug", text_color, letter_color, text_back, letter_back, text_case, letter_case)

def critical(*, text, text_color="red", letter_color="red", text_back=None, letter_back=None, text_case=None, letter_case="upper"):
    return log_message(text, "Critical", text_color, letter_color, text_back, letter_back, text_case, letter_case)


def custom(*, text, log_level, text_color, letter_color, text_back=None, letter_back=None, text_case=None, letter_case="upper"):
    return log_message(text, log_level, text_color, letter_color, text_back, letter_back, text_case, letter_case)