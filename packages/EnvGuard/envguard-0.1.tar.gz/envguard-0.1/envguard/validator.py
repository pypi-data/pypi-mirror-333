import os
from dotenv import load_dotenv

class EnvValidator:
    def __init__(self, env_file='.env', required_vars=None):
        """
        Initialize the validator.
        :param env_file: Path to the .env file
        :param required_vars: List of required environment variables
        """
        self.env_file = env_file
        self.required_vars = required_vars or []
        load_dotenv(self.env_file)

    def check_missing_vars(self):
        """
        Check for missing required environment variables.
        :return: List of missing variables
        """
        missing = []
        for var in self.required_vars:
            if not os.getenv(var):
                missing.append(var)
        return missing

    def validate(self):
        """
        Validate the environment variables.
        :return: Tuple of (missing_vars, is_valid)
        """
        missing = self.check_missing_vars()
        return missing, len(missing) == 0