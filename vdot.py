#!/usr/bin/python3

import argparse
import datetime

from datetime import timedelta
from typing import Dict, Optional

from tables import PACE_TABLE, VDOT_TABLE


class EPace:
    def __init__(self, min_: str, max_: str):
        self.min = to_mile_pace('mile', parse_pace(min_))
        self.max = to_mile_pace('mile', parse_pace(max_))

    def __str__(self):
        return f'E:\t{self.min}/mile - {self.max}/mile'


class MPace:
    def __init__(self, pace: str):
        self.pace = to_mile_pace('mile', parse_pace(pace))

    def __str__(self):
        return f'M:\t{self.pace}/mile'


class TPace:
    def __init__(self, four_hundred: str, km: str, mile: str):
        self.four_hundred = to_mile_pace('400', parse_pace(four_hundred))
        self.km = to_mile_pace('km', parse_pace(km))
        self.mile = to_mile_pace('mile', parse_pace(mile))

    def __str__(self):
        s = 'T:'
        s += f'\t400\t{self.four_hundred}/mile'
        s += f'\n\tkm\t{self.km}/mile'
        s += f'\n\tmile\t{self.mile}/mile'
        return s


class IPace:
    def __init__(
        self, four_hundred: str, km: Optional[str] = None, mile: Optional[str] = None
    ):
        self.four_hundred = to_mile_pace('400', parse_pace(four_hundred))
        if km:
            self.km = to_mile_pace('km', parse_pace(km))
        else:
            self.km = None
        if mile:
            self.mile = to_mile_pace('mile', parse_pace(mile))
        else:
            self.mile = None

    def __str__(self):
        s = 'I:'
        s += f'\t400\t{self.four_hundred}/mile'
        if self.km:
            s += f'\n\tkm\t{self.km}/mile'
        if self.mile:
            s += f'\n\tmile\t{self.mile}/mile'
        return s


class RPace:
    def __init__(self, two_hundred: str, four_hundred: Optional[str] = None):
        self.two_hundred = to_mile_pace('200', parse_pace(two_hundred))
        if four_hundred:
            self.four_hundred = to_mile_pace('400', parse_pace(four_hundred))
        else:
            self.four_hundred = None

    def __str__(self):
        s = 'R:'
        s += f'\t200\t{self.two_hundred}/mile'
        if self.four_hundred:
            s += f'\n\t400\t{self.four_hundred}/mile'
        return s


class PaceSet:
    def __init__(self, table: dict):
        self.e = EPace(table['E']['min'], table['E']['max'])
        self.m = MPace(table['M'])
        self.t = TPace(table['T']['400'], table['T']['km'], table['T']['mile'])
        self.i = IPace(table['I']['400'], table['I']['km'], table['I']['mile'])
        self.r = RPace(table['R']['200'], table['R']['400'])

    def __str__(self):
        return '\n'.join([str(x) for x in [self.e, self.m, self.t, self.i, self.r]])


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


def parse_pace(time: str) -> timedelta:
    ref = datetime.datetime(year=1900, month=1, day=1)
    return datetime.datetime.strptime(time, '%M:%S') - ref


def lookup_vdot(distance: str, time: timedelta) -> int:
    for vdot, paces in VDOT_TABLE.items():
        for d, t in paces.items():
            if distance == d and time <= parse_time(t):
                return vdot
    return 0


def lookup_paces(vdot: int) -> Dict:
    return PACE_TABLE[vdot]


def to_mile_pace(distance: str, time: timedelta) -> timedelta:
    # METERS_PER_MILE = 1609.344
    METERS_PER_MILE = 1600  # close enough for track usage
    if distance == '200':
        return (METERS_PER_MILE / 200) * time
    if distance == '400':
        return (METERS_PER_MILE / 400) * time
    elif distance == 'km':
        return (METERS_PER_MILE / 1000) * time
    elif distance == 'mile':
        return time


def main(args: argparse.Namespace):
    reference_distance = args.distance
    reference_time = parse_time(args.time)

    print(
        f'Calculating VDOT values using reference race distance of {reference_distance} in {reference_time}'
    )

    vdot = lookup_vdot(reference_distance, reference_time)
    print(f'VDOT is {vdot}')

    paces = lookup_paces(vdot)
    pace_set = PaceSet(paces)
    print(pace_set)


if __name__ == '__main__':
    main(parse_args())
