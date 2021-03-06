"""Tests for neighborlist generation."""
import unittest
import os
import numpy as np

from ase.ga.data import DataConnection
from ase.data import covalent_radii

from catlearn.utilities.neighborlist import (ase_neighborlist,
                                             catlearn_neighborlist)
from catlearn.utilities.distribution import pair_distribution, pair_deviation

wkdir = os.getcwd()


class TestNeighborList(unittest.TestCase):
    """Test out the various neighborlist generation routines."""

    def test_ase_nl(self):
        """Function to test the ase wrapper."""
        # Connect database generated by a GA search.
        gadb = DataConnection('{}/data/gadb.db'.format(wkdir))

        # Get all relaxed candidates from the db file.
        all_cand = gadb.get_all_relaxed_candidates(use_extinct=False)

        nl = ase_neighborlist(all_cand[0])

        self.assertEqual(len(all_cand[0]), len(nl))

    def test_catlearn_nl(self):
        """Function to test the ase wrapper."""
        # Connect database generated by a GA search.
        gadb = DataConnection('{}/data/gadb.db'.format(wkdir))

        # Get all relaxed candidates from the db file.
        all_cand = gadb.get_all_relaxed_candidates(use_extinct=False)

        nl1 = catlearn_neighborlist(all_cand[0], max_neighbor=1)
        self.assertEqual((len(all_cand[0]), len(all_cand[0])), np.shape(nl1))
        nl4 = catlearn_neighborlist(all_cand[0], max_neighbor=4)
        self.assertFalse(np.allclose(nl1, nl4))

        nl5 = catlearn_neighborlist(all_cand[0], max_neighbor=5)
        nlfull = catlearn_neighborlist(all_cand[0], max_neighbor='full')
        self.assertFalse(np.allclose(nl4, nl5))
        self.assertTrue(np.allclose(nl5, nlfull))

    def test_pdf(self):
        gadb = DataConnection('{}/data/gadb.db'.format(wkdir))
        all_cand = gadb.get_all_relaxed_candidates(use_extinct=False)

        cutoff_dictionary = {}
        for z in range(1, 92):
            cutoff_dictionary[z] = covalent_radii[z]

        pdf, x1 = pair_distribution(all_cand)

        # Get bond length deviations from touching spheres.
        dev, x2 = pair_deviation(all_cand,
                                 cutoffs=cutoff_dictionary)


if __name__ == '__main__':
    unittest.main()
