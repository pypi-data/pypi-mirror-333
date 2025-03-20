import argparse

from quark.plugin_manager import factory, loader
import yaml

def create_benchmark_parser(parser: argparse.ArgumentParser):
    parser.add_argument("-c", "--config", help="Provide valid config file instead of interactive mode")
    parser.add_argument('-cc', '--createconfig', help='If you want o create a config without executing it',
                        required=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('-s', '--summarize', nargs='+', help='If you want to summarize multiple experiments',
                        required=False)
    parser.add_argument('-m', '--modules', help="Provide a file listing the modules to be loaded")
    parser.add_argument('-rd', '--resume-dir', nargs='?', help='Provide results directory of the job to be resumed')
    parser.add_argument('-ff', '--failfast', help='Flag whether a single failed benchmark run causes QUARK to fail',
                        required=False, action=argparse.BooleanOptionalAction)

    parser.set_defaults(goal='benchmark')



def start() -> None:
    """
    Main function that triggers the benchmarking process
    """

    print(" ============================================================ ")
    print(r"             ___    _   _      _      ____    _  __           ")
    print(r"            / _ \  | | | |    / \    |  _ \  | |/ /           ")
    print(r"           | | | | | | | |   / _ \   | |_) | | ' /            ")
    print(r"           | |_| | | |_| |  / ___ \  |  _ <  | . \            ")
    print(r"            \__\_\  \___/  /_/   \_\ |_| \_\ |_|\_\           ")
    print("                                                              ")
    print(" ============================================================ ")
    print("  A Framework for Quantum Computing Application Benchmarking  ")
    print("                                                              ")
    print("        Licensed under the Apache License, Version 2.0        ")
    print(" ============================================================ ")

    parser = argparse.ArgumentParser()
    create_benchmark_parser(parser)

    args = parser.parse_args()

    with open(args.config) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    loader.load_plugins(data["plugins"])

    pipeline = [factory.create(name, data["pipeline"][name]) for name in data["pipeline"]]

    last_result = None
    for module in pipeline:
        last_result = module.preprocess(last_result)

    last_result = None
    for module in reversed(pipeline):
        last_result = module.postprocess(last_result)

    print(f"Result: {last_result}")
    print(" ============================================================ ")
    print(" ====================  QUARK finished!   ==================== ")
    print(" ============================================================ ")
    exit(0)



if __name__ == '__main__':
    start()
