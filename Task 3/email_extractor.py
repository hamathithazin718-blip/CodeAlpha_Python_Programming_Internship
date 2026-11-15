"""
Email Extraction Automation Utility.

A command-line automation tool that parses plain-text files, extracts unique,
valid email addresses using regular expressions, and exports the normalized
results to a designated output file.
"""

import argparse
import logging
import re
from pathlib import Path
from typing import List

# Configure professional console logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# RFC-compliant simplified regular expression for standard email addresses
EMAIL_REGEX = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")


def initialize_sample_file(file_path: Path) -> None:
    """
    Create a default sample input file if the target input file does not exist.

    Args:
        file_path (Path): The path where the sample file should be created.
    """
    sample_text = (
        "Subject: Internship Task 3 - Project Submission\n\n"
        "Dear Team,\n"
        "Please submit all completed Python automation deliverables to "
        "hamathithazin.718@gmail.com by end of day.\n"
        "For technical escalations, copy support.desk@example.org or "
        "hr-records@company.co.in.\n"
        "Duplicate check: HAMATHITHAZIN.718@GMAIL.COM\n\n"
        "Best regards,\n"
        "Operations Team\n"
    )
    file_path.write_text(sample_text, encoding="utf-8")
    logger.info("Generated default input file at '%s'.", file_path)


def extract_unique_emails(content: str) -> List[str]:
    """
    Extract, normalize (lowercase), and deduplicate email addresses from text.

    Args:
        content (str): Raw text content to scan.

    Returns:
        List[str]: A sorted list of unique, lowercase email addresses.
    """
    raw_matches = EMAIL_REGEX.findall(content)
    normalized_emails = sorted({email.lower() for email in raw_matches})
    return normalized_emails


def process_email_extraction(input_path: Path, output_path: Path) -> None:
    """
    Orchestrate reading the input file, extracting emails, and saving results.

    Args:
        input_path (Path): Path to the source .txt file.
        output_path (Path): Path to the destination .txt file.
    """
    try:
        if not input_path.exists():
            logger.warning("Input file '%s' not found.", input_path)
            initialize_sample_file(input_path)

        logger.info("Reading content from '%s'...", input_path)
        content = input_path.read_text(encoding="utf-8")

        emails = extract_unique_emails(content)

        if not emails:
            logger.warning("No valid email addresses were found in '%s'.", input_path)
            return

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(emails) + "\n", encoding="utf-8")

        logger.info(
            "Successfully extracted %d unique email(s) to '%s'.",
            len(emails),
            output_path,
        )
        for index, email in enumerate(emails, start=1):
            logger.info("  %d. %s", index, email)

    except PermissionError:
        logger.error("Permission denied while accessing files. Check file locks.")
    except OSError as exc:
        logger.error("File system error occurred: %s", exc)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for custom input and output file paths.

    Returns:
        argparse.Namespace: Parsed CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description="Extract unique email addresses from a text file."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=Path("sample_text.txt"),
        help="Path to the input text file (default: sample_text.txt)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("extracted_emails.txt"),
        help="Path to save extracted emails (default: extracted_emails.txt)",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point for the CLI application."""
    args = parse_arguments()
    process_email_extraction(input_path=args.input, output_path=args.output)


if __name__ == "__main__":
    main()
