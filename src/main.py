from functools import partial


class MarkdownEditor:
    def __init__(self) -> None:
        self.markdown = ""

    @staticmethod
    def print_help_text() -> None:
        print("Available formatters:", MarkdownEditor.get_available_formatters())
        print("Special commands:", MarkdownEditor.get_special_commands())

    @staticmethod
    def done(markdown: str) -> None:
        with open("output.md", "w", encoding="utf-8") as file_out:
            file_out.write(markdown)
        quit()

    @staticmethod
    def get_text() -> str:
        return input("Text: ")

    @staticmethod
    def plain() -> str:
        return MarkdownEditor.get_text()

    @staticmethod
    def bold() -> str:
        return f"**{MarkdownEditor.get_text()}**"

    @staticmethod
    def italic() -> str:
        return f"*{MarkdownEditor.get_text()}*"

    @staticmethod
    def link() -> str:
        label = input("Label: ")
        url = input("URL: ")
        return f"[{label}]({url})"

    @staticmethod
    def newline() -> str:
        return "\n"

    @staticmethod
    def header() -> str:
        while True:
            try:
                level = int(input("Level: "))
                if 1 <= level <= 6:
                    break
                raise ValueError
            except ValueError:
                print("The level should be within the range of 1 to 6")
        text = MarkdownEditor.get_text()
        return f"{'#' * level} {text}\n"

    @staticmethod
    def inline_code() -> str:
        return f"`{MarkdownEditor.get_text()}`"

    @staticmethod
    def get_rows() -> int:
        while True:
            try:
                rows = int(input("Number of rows: "))
                if rows <= 0:
                    raise ValueError
                return rows
            except ValueError:
                print("The number of rows should be greater than zero")

    @staticmethod
    def list(ordered: bool = True) -> str:
        rows = MarkdownEditor.get_rows()
        items = ""
        for row in range(rows):
            current_row = row + 1
            if ordered:
                items += f"{current_row}. {input(f'Row #{current_row}: ')}\n"
            else:
                items += f"* {input(f'Row #{current_row}: ')}\n"
        return items

    @staticmethod
    def get_special_commands() -> str:
        return " ".join(command for command in list(COMMANDS.keys()))

    @staticmethod
    def get_available_formatters() -> str:
        return " ".join(formatter for formatter in list(FORMATTERS.keys()))

    @staticmethod
    def get_user_input() -> str:
        while True:
            user_input = input("Choose a formatter: ")
            if user_input in ALL_ACTIONS:
                return user_input
            print("Unknown formatting type or command")

    def run(self) -> None:
        while True:
            if (user_input := self.get_user_input()) in COMMANDS.keys():
                if user_input == "!done":
                    self.done(self.markdown)
                COMMANDS[user_input]()
            elif user_input in FORMATTERS.keys():
                result = FORMATTERS[user_input]()
                self.markdown += result
                print(self.markdown)


COMMANDS = {
    "!help": MarkdownEditor.print_help_text,
    "!done": partial(MarkdownEditor.done, str),
}

FORMATTERS = {
    "plain": MarkdownEditor.plain,
    "bold": MarkdownEditor.bold,
    "italic": MarkdownEditor.italic,
    "header": MarkdownEditor.header,
    "link": MarkdownEditor.link,
    "inline-code": MarkdownEditor.inline_code,
    "ordered-list": partial(MarkdownEditor.list, True),
    "unordered-list": partial(MarkdownEditor.list, False),
    "new-line": MarkdownEditor.newline
}

ALL_ACTIONS = list(COMMANDS.keys()) + list(FORMATTERS.keys())


def main():
    app = MarkdownEditor()
    app.run()


if __name__ == "__main__":
    main()
