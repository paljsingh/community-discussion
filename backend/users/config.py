import yaml


class Config:

    @classmethod
    def load(cls):
        with open('config.yaml', 'r') as file:
            return yaml.load(file, Loader=yaml.FullLoader) or {}
