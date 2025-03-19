import robocop.linter.reports
from robocop import __version__
from robocop.config import Config


class RobocopVersionReport(robocop.linter.reports.ComparableReport):
    """
    **Report name**: ``version``

    Report that returns Robocop version.

    Example::

        Report generated by Robocop version: 2.0.2
    """

    def __init__(self, config: Config):
        self.name = "version"
        self.description = "Returns Robocop version"
        super().__init__(config)

    def persist_result(self):
        return {"generated_with": __version__}

    def get_report(self, prev_results: dict[str, str]) -> str:
        summary = f"\nReport generated by Robocop version: {__version__}"
        if self.compare_runs and prev_results and prev_results["generated_with"] != __version__:
            summary += f". Previous results generated by Robocop version: {prev_results['generated_with']}"
        return summary
