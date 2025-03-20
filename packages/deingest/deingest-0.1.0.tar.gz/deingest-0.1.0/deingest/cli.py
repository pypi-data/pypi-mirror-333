import click
import logging
import sys
from deingest.core import parse_digest_file, restore_files
from deingest.exceptions import ParseError, RestoreError
from deingest import __version__

logger = logging.getLogger(__name__)

@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-f", "--file", "input_file", required=True, type=click.Path(exists=True, dir_okay=False), help="Path to the digest file.")
@click.option("-o", "--output", "output_dir", required=False, type=click.Path(file_okay=False), default=".", help="Directory to restore files into.")
@click.option("-w", "--overwrite", is_flag=True, help="Overwrite existing files.")
@click.option("-d", "--dry-run", is_flag=True, help="Simulate restoration without writing files.")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging output.")
@click.version_option(__version__, prog_name="github-restore")
def main(input_file, output_dir, overwrite, dry_run, verbose):
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        logger.info(f"Parsing digest file: {input_file}")
        entries = parse_digest_file(input_file)
        logger.info(f"Found {len(entries)} entries.")
    except ParseError as e:
        logger.error(f"Error parsing digest: {e}")
        sys.exit(1)
    try:
        logger.info(f"Restoring files to: {output_dir}")
        restored = restore_files(entries, output_dir, overwrite=overwrite, dry_run=dry_run)
        logger.info(f"Restored {len(restored)} files.")
    except RestoreError as e:
        logger.error(f"Restoration errors: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()