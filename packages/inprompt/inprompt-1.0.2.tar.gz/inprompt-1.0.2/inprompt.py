"""Outputs source code formatted as Markdown code blocks for LLM prompts.

Licensed under the MIT License. See LICENSE for details.

Example usage:
    inprompt path/to/file.py 'src/**/*.py' | pbcopy
"""

import glob

from absl import app
from loguru import logger


def uniquify_filenames(seq: list[str]) -> list[str]:
    """Return a list of filenames with duplicates removed, preserving order."""
    seen = set()
    unique = []
    for x in seq:
        if x not in seen:
            unique.append(x)
            seen.add(x)
    return unique


def read_and_format_source_code(filename: str) -> str:
    """Read a file and wrap its contents as a Markdown code fence."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
        return f"{filename}\n```\n{content}\n```"
    except FileNotFoundError:
        logger.error("File not found: {}", filename)
        raise


def main(argv: list[str]) -> int:
    """Main entry point for the CLI, invoked by absl."""
    if len(argv) < 2:
        logger.error("No files or file patterns specified.")
        logger.info("Usage: inprompt <files or patterns> [<files or patterns> ...]")
        return 2

    file_patterns = argv[1:]
    filenames = []
    for pattern in file_patterns:
        matched_files = sorted(glob.glob(pattern))
        if not matched_files:
            logger.warning("No files matched pattern: {}", pattern)
        filenames.extend(matched_files)

    filenames = uniquify_filenames(filenames)
    if not filenames:
        logger.error("No matching files found.")
        return 3

    formatted_contents = [read_and_format_source_code(fname) for fname in filenames]
    print("\n\n".join(formatted_contents))

    logger.info("Formatted and outputted {} files.", len(filenames))
    return 0


def run():
    """Entry point for the console script (declared in pyproject.toml)."""
    app.run(main)


if __name__ == "__main__":
    # If called directly: `python -m inprompt <patterns>`
    run()
