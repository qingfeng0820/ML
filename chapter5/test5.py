# -*- coding: utf-8 -*-
import optimization


def test_print_schedule():
    s = [1, 4, 3, 2, 7, 3, 6, 3, 2, 4, 5, 3]
    optimization.printschedule(s)


def test_cal_schedule_cost():
    s = [1, 4, 3, 2, 7, 3, 6, 3, 2, 4, 5, 3]
    print optimization.schedulecost(s)


def test_find_optimized_schedule(optimization_method):
    domain = [(0, 8)] * (len(optimization.people) * 2)
    r = optimization_method(domain, optimization.schedulecost)
    optimization.printschedule(r)
    print optimization.schedulecost(r)


if __name__ == "__main__":
    test_find_optimized_schedule(optimization.geneticoptimize)
