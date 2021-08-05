import json
import logging
import random


def get_dataset(filepath):
    try:
        with open(filepath) as fp:
            dataset = list(json.load(fp))
            logging.info("Loaded %s items in dataset", len(dataset))
            return dataset
    except (ValueError, FileNotFoundError):
        return []


def get_random_choice(dataset):
    return random.choice(dataset)


def random_bool():
    return bool(random.randint(0, 1))
