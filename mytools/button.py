import re

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class Button:
    def __init__(self):
        self.url_pattern = r"(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:[/?]\S+)?|tg://\S+$"

    def fetchUrls(self, text):
        return re.findall(self.url_pattern, text)

    def extractButtonsAndText(self, text):
        button_data = re.findall(r"\| ([^|]+) - ([^|]+) \|", text)
        extracted_text = re.split(r"\| [^|]+ - [^|]+ \|", text)[0].strip() if "|" in text else text.strip()
        return button_data, extracted_text

    def buildDynamicInlineKeyboard(self, text, inline_cmd=None, is_id=None):
        keyboard_layout = []
        button_data, extracted_text = self.extractButtonsAndText(text)

        for button_label, button_payload in button_data:
            cb_data, *extra_params = button_payload.split(";")

            if not self.fetchUrls(cb_data):
                cb_data = f"{inline_cmd} {is_id}_{cb_data}" if inline_cmd and is_id else cb_data

            button = (
                InlineKeyboardButton(button_label, user_id=cb_data)
                if "user" in extra_params
                else (
                    InlineKeyboardButton(button_label, url=cb_data)
                    if self.fetchUrls(cb_data)
                    else InlineKeyboardButton(button_label, callback_data=cb_data)
                )
            )

            if "same" in extra_params and keyboard_layout:
                keyboard_layout[-1].append(button)
            else:
                keyboard_layout.append([button])

        return InlineKeyboardMarkup(keyboard_layout), extracted_text

    def generateInlineButtonGrid(self, buttons, row_width=2):
        grid_layout = [
            [InlineKeyboardButton(**button_data) for button_data in buttons[i : i + row_width]]
            for i in range(0, len(buttons), row_width)
        ]
        return InlineKeyboardMarkup(grid_layout)
