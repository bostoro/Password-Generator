import string

class UppercaseStrategy:
    def get_chars(self) -> str:
        return string.ascii_uppercase

class LowercaseStrategy:
    def get_chars(self) -> str:
        return string.ascii_lowercase

class NumberStrategy:
    def get_chars(self) -> str:
        return string.digits

class SymbolStrategy:
    def get_chars(self) -> str:
        return string.punctuation