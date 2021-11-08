import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    return parser.parse_args()


def main(args: argparse.Namespace):
    pass


if __name__ == '__main__':
    main(parse_args())
