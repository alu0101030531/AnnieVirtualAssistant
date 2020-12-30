import re

class InputManager:
    def parse(self, regexp, text):
        return re.search(str(regexp), text)


