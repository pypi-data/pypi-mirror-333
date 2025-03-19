from tests.linter.utils import RuleAcceptance


class TestRuleAcceptance(RuleAcceptance):
    def test_rule(self):
        self.check_rule(
            src_files=["test.robot", "test.resource", "documentation.resource", "with_settings.resource"],
            expected_file="expected_output.txt",
        )

    def test_extended(self):
        self.check_rule(expected_file="expected_extended.txt", output_format="extended")
