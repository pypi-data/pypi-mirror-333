import logging
import logging.config
import yaml


def setup_logging():
    try:
        with open('logging.yaml', 'r') as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)
        logger = logging.getLogger('protoai')
        logger.debug(
            f'{"=" * 51}\n> {"=" * 20} START LOG {"=" * 20}\n> {"=" * 51}'
        )
    except FileNotFoundError as e:
        print(f'Can not find logging config file. \nError: `{e}`')
    except yaml.YAMLError as e:
        print(f'Logging config parse failed. \nError: `{e}`')
