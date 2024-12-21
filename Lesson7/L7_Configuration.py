import logging

# Configure logging for debugging and tracking operations
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Global configuration representing application settings
GLOBAL_CONFIG = {
    "feature_a": True,
    "feature_b": False,
    "max_retries": 3
}


class Configuration:
    def __init__(self, updates, validator=None):
        """Context manager for temporarily modifying the global configuration."""
        # Store the updates and the optional validator
        self.updates = updates
        self.validator = validator
        # To store the original state of the global configuration
        self.original_config = None

    def __enter__(self):
        self.original_config = GLOBAL_CONFIG.copy()
        GLOBAL_CONFIG.update(self.updates)
        logging.info("Changes for debugging purpose: %s", self.updates)

    def __exit__(self, exc_type, exc_value, traceback):
        if self.validator:
            validation = self.validator(GLOBAL_CONFIG)
            if not validation:
                logging.error("Validation failed: %s", GLOBAL_CONFIG)
                GLOBAL_CONFIG.clear()
                GLOBAL_CONFIG.update(self.original_config)
                logging.info("Configuration restored to: %s", GLOBAL_CONFIG)
                return True

        GLOBAL_CONFIG.clear()
        GLOBAL_CONFIG.update(self.original_config)
        logging.info("Configuration restored to: %s", GLOBAL_CONFIG)


def validate_config(config: dict) -> bool:
    if config["max_retries"] < 0:
        return False
    if not isinstance(config["feature_a"], bool):
        return False
    return True


if __name__ == "__main__":
    logging.info("Initial GLOBAL_CONFIG: %s", GLOBAL_CONFIG)

    # Example 1: Successful configuration update
    try:
        with Configuration({"feature_a": False, "max_retries": 5}):
            logging.info("Inside context: %s", GLOBAL_CONFIG)
    except Exception as e:
        logging.error("Error: %s", e)

    logging.info("After context: %s", GLOBAL_CONFIG)

    # Example 2: Configuration update with validation failure
    try:
        with Configuration({"feature_a": "invalid_value", "max_retries": -1}, validator=validate_config):
            logging.info("This should not be printed if validation fails.")
    except Exception as e:
        logging.error("Caught exception: %s", e)

    logging.info("After failed context: %s", GLOBAL_CONFIG)