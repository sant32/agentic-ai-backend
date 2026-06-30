import re


class PIIMaskingService:

    EMAIL_PATTERN = re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    )

    PHONE_PATTERN = re.compile(
        r"\b\d{10}\b"
    )

    def mask(self, text: str) -> str:

        text = self.EMAIL_PATTERN.sub(
            "[EMAIL]",
            text,
        )

        text = self.PHONE_PATTERN.sub(
            "[PHONE]",
            text,
        )

        return text