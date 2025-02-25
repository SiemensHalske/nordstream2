import os
import argparse
from dataclasses import dataclass
import yara  # pylint: disable=import-error

from ns2.logger import CustomLogger

# Initialize the logger
log = CustomLogger(name=__name__)


@dataclass
class Config:
    """Data class to hold configuration."""
    _rule_base: str = "yara_rules"
    rule_base: str = ""

    def __init__(self):
        """
        Initialize the Config class.

        Automatically detects the root directory for the yara rules.
        """
        self.rule_base = self.get_rule_base()

    def get_rule_base(self) -> str:
        """
        Get the root directory for the YARA rules.
        """

        # Check if the rule base is already in the current directory
        if os.path.isdir(self._rule_base):
            return self._rule_base

        # Check if the rule base is in the parent directory
        parent_dir = os.path.join(os.getcwd(), os.pardir)
        rule_base = os.path.join(parent_dir, self._rule_base)
        if os.path.isdir(rule_base):
            return rule_base

        # Check if the rule base is in the grandparent directory
        grandparent_dir = os.path.join(parent_dir, os.pardir)
        rule_base = os.path.join(grandparent_dir, self._rule_base)
        if os.path.isdir(rule_base):
            return rule_base

        # If the rule base is not found, return an empty string
        return ""


@dataclass
class YaraConfig:
    """Data class to hold YARA configuration."""
    rule_path: str
    file_to_scan: str


class YaraScanner:
    """Class to handle YARA rule compilation and file scanning."""

    def __init__(self, rule_path, file_to_scan):
        self.rule_path = rule_path
        self.file_to_scan = file_to_scan
        self.compiled_rule = None

    def validate_paths(self):
        """Validate the paths for the rule file and the file to scan."""
        if not os.path.isfile(self.rule_path):
            # log.error(
            #    f"Rule file not found: {self.rule_path}")
            raise FileNotFoundError(f"Rule file not found: {self.rule_path}")
        if not os.path.isfile(self.file_to_scan):
            log.error(
                f"File to scan not found: {self.file_to_scan}")
            raise FileNotFoundError(
                f"File to scan not found: {self.file_to_scan}")

    def compile_rule(self):
        """Compile the YARA rule."""
        try:
            # keep only the file name
            rule_path_d = self.rule_path.split("\\")[-1].replace(".yar", "")
            log.info(
                f"Compiling YARA rule from: {rule_path_d}"
            )
            self.compiled_rule = yara.compile(filepath=self.rule_path)
        except yara.SyntaxError as e:
            log.error(f"Syntax Error in YARA rule: {e}")
            raise
        except Exception as e:
            log.error(f"Failed to compile YARA rule: {e}")
            raise

    def scan_file(self):
        """Scan the file using the compiled YARA rule."""
        try:
            abs_file_path = os.path.abspath(self.file_to_scan)
            log.info(
                f"Scanning file: {abs_file_path}"
            )
            matches = self.compiled_rule.match(self.file_to_scan)
            return matches
        except yara.Error as e:
            log.error(f"YARA Error while scanning: {e}")
            raise
        except Exception as e:
            log.error(
                f"Unexpected error while scanning: {e}"
            )
            raise


class YaraScannerCLI:
    """Class to handle the CLI interface for the YARA scanner."""

    def __init__(self):
        self.args = self.get_cmd_args()

    def get_cmd_args(self):
        """Get command-line arguments."""

        parser = argparse.ArgumentParser(
            description="CLI tool to scan files using YARA rules.",
            epilog="Created with 💡 and Rich logging!"
        )

        parser.add_argument(
            "-r", "--rule",
            required=True,
            help="Path to the YARA rule file."
        )

        parser.add_argument(
            "-f", "--file",
            required=True,
            help="Path to the file to scan."
        )

        return parser.parse_args()

    def get_rule_path(self, rule_file: str) -> str:
        """Formats the path to the YARA rule file."""
        path: str = ''

        # Check if the rule file has a file extension
        if not rule_file.endswith(".yar") and not rule_file.endswith(".yara"):
            rule_file = f"{rule_file}.yar"

        # Check if the rule file is an absolute path
        if os.path.isabs(rule_file):
            return rule_file

        # Check if the rule file is in the default rules directory
        config = Config()
        rule_base = config.rule_base
        path = os.path.join(rule_base, rule_file)

        return path

    def run(self):
        """Run the CLI tool."""
        rule_path = self.get_rule_path(self.args.rule)
        file_to_scan = self.args.file

        try:
            scanner = YaraScanner(rule_path, file_to_scan)
            scanner.validate_paths()
            scanner.compile_rule()
            matches = scanner.scan_file()

            # Print results
            if matches:
                log.success("YARA rule matched!")
                log.info(matches, success=True)
            else:
                log.warning("[bold yellow]No matches found.[/bold yellow]")

        except FileNotFoundError as e:
            log.error(e)
        except yara.SyntaxError:
            log.error(f"An unexpected error occurred: {e}")
