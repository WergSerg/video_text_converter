"""Утилиты"""

def get_recognized_text_in_html(recognized_text: dict) -> str:
    """Возвращает распознанный текст в формате HTML"""

    return "".join(
        f"<div style='width: 800px'><strong>{min}:</strong> {text}</div><br>"
        for min, text in recognized_text.items()
    )
