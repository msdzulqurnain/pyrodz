import re
from framework.console.style import Style


class Command:
    def confirm(self, message, default=True):
        suffix = "[Y/n]" if default else "[y/N]"

        answer = input(f"{message} {suffix}: ").strip().lower()

        if not answer:
            return default

        return answer in ("y", "yes")
    
    def is_valid_class_name(self, name):
        return bool(re.match(r"^[A-Z][a-zA-Z0-9]*$", name))
    
    def invalid_name(self, name, suffix):
        print()
        print(
            Style.error(
                f'{suffix} "{name}" name must use PascalCase '
                f'(example: {name.capitalize()} or {name.capitalize()}{suffix})'
            )
        )