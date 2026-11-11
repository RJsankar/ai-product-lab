import unittest

from prompts import (
    EVALUATION_SCHEMA,
    PERSONAS,
    customer_input,
    evaluation_input,
    persona_instructions,
)


class PromptTests(unittest.TestCase):
    def setUp(self):
        self.persona = next(iter(PERSONAS))
        self.scenario = "A discovery call for an AI coaching product."
        self.messages = [
            {"role": "assistant", "content": "What would you like to discuss?"},
            {"role": "user", "content": "How do you coach your team today?"},
        ]

    def test_persona_prompt_contains_selected_context(self):
        prompt = persona_instructions(self.persona, self.scenario)
        self.assertIn(self.persona, prompt)
        self.assertIn(self.scenario, prompt)
        self.assertIn("Stay in character", prompt)

    def test_transcript_labels_roles(self):
        self.assertIn("Sales rep:", customer_input(self.messages))
        self.assertIn("Customer:", evaluation_input(self.messages))

    def test_evaluation_schema_is_strict(self):
        self.assertFalse(EVALUATION_SCHEMA["additionalProperties"])
        self.assertEqual(EVALUATION_SCHEMA["properties"]["overall_score"]["maximum"], 5)


if __name__ == "__main__":
    unittest.main()

