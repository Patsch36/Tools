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
        offset = 0  # Scroll-Offset

        while True:
            height, width = stdscr.getmaxyx()
            visible_items = self.get_visible_items(height, input_text, offset)
            total_items = len(visible_items)

            if total_items > 0:
                current_row = min(current_row, total_items - 1)

            stdscr.clear()
            self.display_menu(stdscr, visible_items, current_row, input_text)
            stdscr.refresh()

            key = stdscr.getch()
            current_row, input_text, offset, selection_made = self.handle_key_press(
                key, current_row, input_text, total_items, height, offset)

            if selection_made:
                return self.finalize_selection(visible_items, current_row, input_text)

    def get_visible_items(self, height: int, input_text: str, offset: int) -> List[str]:
        filtered_items = self.filter_items(input_text)
        max_displayable = height - 4  # Platz für die Eingabezeile und Anweisung
        return filtered_items[offset:offset + max_displayable]

    def display_menu(self, stdscr, visible_items: List[str], current_row: int, input_text: str):
        stdscr.addstr(0, 0, self.prompt)
        for idx, item in enumerate(visible_items):
            if idx == current_row:
                stdscr.addstr(
                    idx + 1, 0, f"{idx + 1}. {item}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 1, 0, f"{idx + 1}. {item}")

        stdscr.addstr(len(visible_items) + 2, 0,
                      "Oder geben Sie eine eigene Eingabe ein:")
        stdscr.addstr(len(visible_items) + 3, 0, input_text)

    def handle_key_press(self, key: int, current_row: int, input_text: str, total_items: int, height: int, offset: int) -> tuple[int, str, int, bool]:
        max_displayable = height - 4
        if key == curses.KEY_UP:
            if current_row > 0:
                current_row -= 1
            elif offset > 0:
                offset -= 1
        elif key == curses.KEY_DOWN:
            if current_row < min(total_items - 1, max_displayable - 1):
                current_row += 1
            elif offset + max_displayable < total_items:
                offset += 1
        elif key in (curses.KEY_ENTER, 10, 13):  # Enter-Taste
            return current_row, input_text, offset, True
        elif key in (curses.KEY_BACKSPACE, 127, 8):  # Backspace-Taste
            input_text = input_text[:-1]
        elif 32 <= key <= 126:  # Druckbare Zeichen
            input_text += chr(key)
            offset = 0  # Zurücksetzen des Scrolls nach neuer Eingabe
        return current_row, input_text, offset, False

    def filter_items(self, input_text: str) -> List[str]:
        if not input_text:
            return self.items
        words = input_text.lower().split()
        return [item for item in self.items if all(word in item.lower() for word in words)]

    def finalize_selection(self, visible_items: List[str], current_row: int, input_text: str) -> Optional[str]:
        if visible_items:
            return visible_items[current_row]
        return input_text

    def select(self):
        return curses.wrapper(self.navigate_menu)
