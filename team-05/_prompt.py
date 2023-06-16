import warnings
from pathlib import Path


class Prompt:
    def __init__(self, prompt_path: Path, subs_pattern: str = "<>"):
        assert prompt_path.exists(), "Prompt file does not exist"
        assert len(subs_pattern) == 2, "Substitution pattern must be of length 2," \
                                       " each character representing the start and end of a substitution"

        # Load prompt text
        with open(prompt_path, "r") as prompt_f:
            self.base = prompt_f.read()
        self.subs_pattern = subs_pattern

        # Find initial substitutions
        self.subs = self._find_subs(self.base)

        # Full Prompt
        self.prompt = self.base

    def __str__(self):
        # For ease of casting, printing, debugging
        if self._find_subs(self.prompt):
            warnings.warn("Prompt still contains substitutions")
        return self.prompt

    def _find_subs(self, text: str) -> list[str]:
        # Find substitutions(enclosed by the first and second character of the subs_pattern)
        subs, start = [], None
        for i, char in enumerate(text):
            if char == self.subs_pattern[0]:
                start = i
            elif char == self.subs_pattern[1] and start is not None:
                subs.append(text[start + 1:i])
                start = None
        return subs

    def reset(self) -> None:
        # Reset prompt to base
        self.prompt = self.base
        self.subs = self._find_subs(self.prompt)

    def substitute(self, subs_key: str, subs_value: str) -> None:
        assert subs_key in self.subs, f"Substitution key {subs_key} not found in prompt"

        # Substitute text in prompt
        full_key = self.subs_pattern[0] + subs_key + self.subs_pattern[1]
        self.prompt = self.prompt.replace(full_key, subs_value)
        self.subs.remove(subs_key)
