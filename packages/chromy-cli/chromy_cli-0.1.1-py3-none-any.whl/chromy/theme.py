from inquirer.themes import Theme
from blessed import Terminal

term = Terminal()


class CoolTheme(Theme):
    def __init__(self):
        super().__init__()
        self.Question.mark_color = term.color_rgb(0, 71, 171)
        self.Question.brackets_color = term.normal
        self.Question.default_color = term.normal
        self.Editor.opening_prompt_color = term.bright_black
        self.Checkbox.selection_color = term.cyan
        self.Checkbox.selection_icon = "->"
        self.Checkbox.selected_icon = "✓"
        self.Checkbox.selected_color = term.color_rgb(135, 206, 235) + term.bold
        self.Checkbox.unselected_color = term.normal
        self.Checkbox.unselected_icon = "✗"
        self.Checkbox.locked_option_color = term.gray50
        self.List.selection_color = term.cyan
        self.List.selection_cursor = ">"
        self.List.unselected_color = term.normal