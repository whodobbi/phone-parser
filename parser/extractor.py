import re
from loguru import logger


class PhoneExtractor:
    """Extract and normalize phone numbers from a text file."""

    def __init__(self, filepath: str) -> None:
        """Initialize parser with file path."""
        self.filepath = filepath
        logger.info(f"Initializing with file: {filepath}")
        self.raw_text = self._read_file()
        self.numbers: list[str] = []

    def _read_file(self) -> str:
        """Read text file content."""
        logger.info(f"Reading file: {self.filepath}")
        try:
            with open(self.filepath, encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            logger.error(f"File not found: {self.filepath}")
            raise
        logger.success("File read successfully")
        return content

    def extract(self) -> list[str]:
        """Extract and return unique normalized phone numbers."""
        formatted = [
            normalized for num in self._find_phones(self.raw_text)
            if (normalized := self._normalize(num))
        ]

        seen = set()
        result = []

        for number in formatted:
            if number not in seen:
                seen.add(number)
                result.append(number)

        self.numbers = result
        logger.success(f"Unique numbers found: {len(self.numbers)}")
        return self.numbers

    def _find_phones(self, text: str) -> list[str]:
        """Find potential phone numbers in text."""
        pattern = re.compile(
            r"(?:\+7|8)[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{3,4}[\s\-\.]?\d{2}[\s\-\.]?\d{2,4}",
            re.UNICODE,
        )
        matches = pattern.findall(text)
        logger.info(f"Found {len(matches)} potential phone numbers")
        return matches

    def _normalize(self, raw_phone: str) -> str:
        """Normalize phone number to +7(YYY)XXX-XX-XX format."""
        digits = re.sub(r"\D", "", raw_phone)

        if digits.startswith("8"):
            digits = "7" + digits[1:]
        elif digits.startswith("7"):
            digits = "7" + digits[1:]
        elif digits.startswith("9"):
            digits = "7" + digits

        if len(digits) != 11:
            logger.warning(f"Invalid phone number: {raw_phone}")
            return ""
        formatted = f"+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
        logger.debug(f"Normalized phone number: {formatted}")
        return formatted