import string, random
from typing import List, Optional

from app.utils.data_handlers import ConfigurationDataHandler
from app.utils.exceptions import ErrorException
from .base import BaseService


class PasswordGeneratorService(BaseService):

    LOWERCASE_CHARS = list(string.ascii_lowercase)
    UPPERCASE_CHARS = list(string.ascii_lowercase.upper())
    NUMBERS = list(string.digits)
    SPECIAL_SYMBOLS = list(string.punctuation)

    def __init__(
        self,
        lenght: int,
        numbers: bool,
        lowercase_chars: bool,
        uppercase_chars: bool,
        special_symbols: bool,
        configuration_data_handler: ConfigurationDataHandler,
    ) -> None:
        super().__init__()
        self.lenght: int = lenght
        self.numbers: bool = numbers
        self.lowercase_chars: bool = lowercase_chars
        self.uppercase_chars: bool = uppercase_chars
        self.special_symbols: bool = special_symbols
        self.configuration_data_handler: ConfigurationDataHandler = (
            configuration_data_handler
        )
        self.password: Optional[str] = None

    def run(self) -> None:
        self._validate_params()
        self._generate_password()
        pass

    def _validate_params(self) -> None:
        exception = ErrorException(
            "one of the following parameters must be provided: 'numbers', 'lowercase_chars', 'uppercase_chars' or 'special_symbols'"
        )
        if (
            not self.numbers
            and not self.lowercase_chars
            and not self.uppercase_chars
            and not self.special_symbols
        ):
            raise exception

    def _get_char_types(self) -> List[List[str]]:
        active_config = self.configuration_data_handler.get_active_config
        if not active_config:
            raise ErrorException("there is no active configuration")

        char_types = list()

        if self.numbers is True:
            char_types.append(self.NUMBERS)
        elif self.numbers is None:
            if active_config.numbers:
                char_types.append(self.NUMBERS)

        if self.lowercase_chars is True:
            char_types.append(self.LOWERCASE_CHARS)
        elif self.lowercase_chars is None:
            if active_config.lowercase_chars:
                char_types.append(self.LOWERCASE_CHARS)

        if self.uppercase_chars is True:
            char_types.append(self.UPPERCASE_CHARS)
        elif self.uppercase_chars is None:
            if active_config.uppercase_chars:
                char_types.append(self.UPPERCASE_CHARS)

        if self.special_symbols is True:
            char_types.append(self.SPECIAL_SYMBOLS)
        elif self.special_symbols is None:
            if active_config.special_symbols:
                char_types.append(self.SPECIAL_SYMBOLS)

        return char_types

    def _generate_password(self) -> None:
        char_types = self._get_char_types()
        final_password = ""

        # get configured default lenght if not provided
        if self.lenght:
            lenght = self.lenght
        else:
            lenght = self.configuration_data_handler.get_active_config.lenght

        for _ in range(lenght):
            random_char_type = random.choice(char_types)
            final_password += random.choice(random_char_type)
        self.password = final_password
