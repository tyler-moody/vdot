#!/usr/bin/python3

import argparse
import datetime

from datetime import timedelta

from tables import VDOT_TABLE


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('distance', choices=['5k'], help='The reference race distance')
    parser.add_argument(
        'time', type=str, help='The reference race time, in HH:MM:SS format'
    )
    return parser.parse_args()


def parse_time(time: str) -> timedelta:
    ref = datetime.datetime(year=1900, month=1, day=1)
    return datetime.datetime.strptime(time, '%H:%M:%S') - ref


def lookup_vdot(distance: str, time: timedelta) -> int:
    for vdot, paces in VDOT_TABLE.items():
        for d, t in paces.items():
            if distance == d and time <= t:
                return vdot
    return 0


def main(args: argparse.Namespace):
    reference_distance = args.distance
    reference_time = parse_time(args.time)

    print(
        f'Calculating VDOT values using reference race distance is {reference_distance} in {reference_time}'
    )

    vdot = lookup_vdot(reference_distance, reference_time)
    print(f'VDOT is {vdot}')


if __name__ == '__main__':
    main(parse_args())
