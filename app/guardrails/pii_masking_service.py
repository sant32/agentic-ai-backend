class PromptInjectionService:

    BLOCKED_PATTERNS = [
        "ignore previous instructions",
        "ignore all instructions",
        "forget previous instructions",
        "reveal system prompt",
        "show system prompt",
        "print system prompt",
        "developer message",
        "execute code",
        "run shell command",
        "bypass safety",
    ]

    def detect(
        self,
        text: str,
    ) -> bool:

        text = text.lower()

        for pattern in self.BLOCKED_PATTERNS:

            if pattern in text:
                return True

        return False

    def validate(
        self,
        text: str,
    ):

        if self.detect(text):
            raise ValueError(
                "Prompt injection attempt detected."
            )