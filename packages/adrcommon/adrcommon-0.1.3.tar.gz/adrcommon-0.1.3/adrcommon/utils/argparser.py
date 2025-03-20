import argparse


class ArgParser(object):
    def get_arg(self, key):
        parser = argparse.ArgumentParser()
        parser.add_argument(f'--{key}')

        args = vars(parser.parse_args())
        return args[key]
