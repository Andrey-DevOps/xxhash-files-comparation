import yaml
import argparse
from sys import modules
import pathlib
import importlib
def load_plugin(config):
    plugin = importlib.import_module("plugins.{0}".format(yaml_config["source"][0]["type"]), package=None)
    plugin.run(yaml_config)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="xxhash-file-comparation",description= "This program helps to compare hashes between source and destination after download.")
    parser.add_argument("-c","--config")

    args = (parser.parse_args())
    config_path=str(args.config)

    if config_path != "None" and pathlib.Path(config_path).exists():
        config_path = pathlib.Path(config_path).absolute()
        with open(config_path, "r") as f:
            yaml_config = yaml.load(f, Loader=yaml.FullLoader)
    else:
        config_path = str(pathlib.Path(str((modules['__main__'].__file__))).parents[0])+"/config.yaml"
        with open(config_path, "r") as f:
            yaml_config = yaml.load(f, Loader=yaml.FullLoader)
    load_plugin(yaml_config)






