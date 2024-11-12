import curses
from typing import List, Optional


class MenuSelector:
    def __init__(self, items: List[str], prompt: str = "Wähle eine Option oder gebe eine eigene Eingabe ein:"):
        self.items = items
        self.prompt = prompt

    def navigate_menu(self, stdscr) -> Optional[str]:
        curses.curs_set(0)
        current_row = 0
        input_text = ""

        while True:
            # Filtere die Liste basierend auf der Eingabe
            filtered_items = self.filter_items(input_text)
            total_items = len(filtered_items)

            # Stelle sicher, dass current_row im gültigen Bereich bleibt
            if total_items > 0:
                current_row = min(current_row, total_items - 1)

            stdscr.clear()
            self.display_menu(stdscr, filtered_items, current_row, input_text)
            stdscr.refresh()

            key = stdscr.getch()
            current_row, input_text, selection_made = self.handle_key_press(
                key, current_row, input_text, total_items)

            if selection_made:
                return self.finalize_selection(filtered_items, current_row, input_text)

    def display_menu(self, stdscr, filtered_items: List[str], current_row: int, input_text: str):
        stdscr.addstr(0, 0, self.prompt)
        for idx, item in enumerate(filtered_items):
            if idx == current_row:
                stdscr.addstr(
                    idx + 1, 0, f"{idx + 1}. {item}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 1, 0, f"{idx + 1}. {item}")

        stdscr.addstr(len(filtered_items) + 2, 0,
                      "Oder geben Sie eine eigene Eingabe ein:")
        stdscr.addstr(len(filtered_items) + 3, 0, input_text)

    def handle_key_press(self, key: int, current_row: int, input_text: str, total_items: int) -> tuple[int, str, bool]:
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < total_items - 1:
            current_row += 1
        elif key in (curses.KEY_ENTER, 10, 13):  # Enter-Taste
            return current_row, input_text, True
        elif key in (curses.KEY_BACKSPACE, 127, 8):  # Backspace-Taste
            input_text = input_text[:-1]
        elif 32 <= key <= 126:  # Druckbare Zeichen
            input_text += chr(key)
        return current_row, input_text, False

    def filter_items(self, input_text: str) -> List[str]:
        if not input_text:
            return self.items
        return [item for item in self.items if input_text.lower() in item.lower()]

    def finalize_selection(self, filtered_items: List[str], current_row: int, input_text: str) -> Optional[str]:
        if filtered_items:
            return filtered_items[current_row]
        return input_text

    def select(self):
        return curses.wrapper(self.navigate_menu)
