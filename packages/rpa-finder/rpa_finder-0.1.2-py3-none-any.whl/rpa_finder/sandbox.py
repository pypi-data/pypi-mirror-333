from ReactionSystem import ReactionSystem
from ReactionSystem import from_lbs_to_bs

import numpy as np


def test_network(network):
    system = ReactionSystem(network)

    lbs = system.enumerate_labeled_buffering_structures()
    lbs_name = [ system.lbs_to_name(l) for l in lbs]

    print('\nlabeled buffering structures')
    for l in lbs_name:
        print(l)

    bs = list(map(from_lbs_to_bs, lbs))
    print('\nbuffering structures')
    for b in bs:
        print(b)

    print('\ninfluence index')
    for b in bs:
        print(system.compute_influence_index(b))



if __name__ == "__main__":  # pragma: no cover


    # 1
    test_network([
                    ['','"x"'],
                    ['"x"','"y"'],
                    ['"y"',''],
                ])
    
    # 2
    test_network(
        [
            ['', '"v1"'],
            ['','"v2"'],
            ['"v1"','"v3"'],
            ['"v2"','"v4"'],
            ['"v3"','"v4"'],
            ['"v3"','"v5"'],
            ['"v4"','"v6"'],
            ['"v6"','"v5"'],
            ['"v5"','"v7"'],
            ['"v6"','"v8"'],
            ['"v7"','"v3"'],
            ['"v7"+"v8"','"v9"'],
            ['"v6"',''],
            ['"v9"','']
        ]
    )

    # 3
    test_network(
        [
            ['', '"v1"'],
            ['"v1"','"v2"'],
            ['"v2"','"v3"'],
            ['"v3"','"v1"'],
            ['"v2"','']
        ]
    )

    # 4
    test_network(
        [
            ['', '"v1"'],
            ['2"v1"','"v2"'],
            ['"v2"','"v3"'],
            ['"v3"','"v1"'],
            ['"v2"','']
        ]
    )


    # 5 antithetic 2
    test_network(
        [
            ['"z1"', '"z1"+"x"'],
            ['"z1"+"z2"',''],
            ['','"z1"'],
            ['2"x"','2"x"+"z2"'],
            ['"x"',''],
            ['"y"','"y"+"z1"'],
            ['','"y"'],
            ['"y"','']
        ]
    )

    # 6 example with a conserved quantity
    test_network(
        [
            ['0', '"v1"'],
            ['"v1"','"v2"'],
            ['"v2"','0'],
            ['"v1"+"v2"','"v3"+"v4"'],
            ['"v3"+"v4"','"v1"+"v2"']
        ]
    )

    # 7 bacterial chemotaxis
    test_network(
        [
            ['"xms"', '"xm"'],
            ['"xm"','"xms"'],
            ['','"xm"'],
            ['','"xms"'],
            ['"xms"','']
        ]
    )

    # 8 yeast metabolism
    test_network(
        [
            ['"Glucose"', '"G6P"'],
            ['"G6P"', '"F6P"'],
            ['"F6P"', '"G6P"'],
            ['"F6P"', '"F16P"'],
            ['"F16P"', '"G3P" + "DHAP"'],
            ['"DHAP"', '"G3P"'],
            ['"G3P"', '"PGP"'],
            ['"PGP"', '"PG3"'], ['"PG3"', '"PGP"'],
            ['"PG3"', '"PG2"'], ['"PG2"', '"PG3"'],
            ['"PG2"', '"PEP"'],
            ['"PEP"', '"PG2"'],
            ['"PEP"', '"PYR"'],
            ['"G6P"', '"PG6"'],
            ['"PG6"', '"Ru5P" + "CO2"'],
            ['"Ru5P"', '"X5P"'],
            ['"Ru5P"', '"R5P"'],
            ['"X5P" + "R5P"', '"G3P" + "S7P"'],
            ['"G3P" + "S7P"', '"X5P" + "R5P"'],
            ['"G3P" + "S7P"', '"F6P" + "E4P"'],
            ['"F6P" + "E4P"', '"G3P" + "S7P"'],
            ['"X5P" + "E4P"', '"F6P" + "G3P"'],
            ['"F6P" + "G3P"', '"X5P" + "E4P"'],
            ['"PG6"', '"G3P" + "PYR"'],
            ['"PYR"', '"Acetal" + "CO2"'],
            ['"Acetal"', '"Ethanol"'],
            ['"Ethanol"', '"Acetal"'],
            ['"R5P"', ''],
            ['"CO2"', ''],
            ['', '"Glucose"'],
            ['"Ethanol"', ''],
            ['"Acetal"', ''],
            ['"PYR"', '"Ala"'],
            ['"Ala"', '"PYR"'],
            ['"Ala"', ''],
        ]
    )

