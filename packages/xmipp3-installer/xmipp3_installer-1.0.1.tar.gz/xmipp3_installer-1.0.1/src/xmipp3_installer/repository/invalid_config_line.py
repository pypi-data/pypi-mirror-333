"""### Contains a custom exception for lines in the configuration file with invalid format."""

from xmipp3_installer.application.logger.logger import logger

class InvalidConfigLineError(RuntimeError):
  @staticmethod
  def generate_error_message(config_file, line_number, line):
    return '\n'.join([
      logger.yellow(f"WARNING: There was an error parsing {config_file} file: "),
      logger.red(f'Unable to parse line {line_number}: {line}'),
      logger.yellow(
        "Contents of config file won't be read, default values will be used instead.\n"
        f"You can create a new file template from scratch deleting file {config_file} and trying again."
      )
    ])
