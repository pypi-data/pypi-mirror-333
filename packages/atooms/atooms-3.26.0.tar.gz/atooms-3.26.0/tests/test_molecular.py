#!/usr/bin/env python

import os
import unittest
from atooms.trajectory import TrajectoryLAMMPS, MolecularTrajectoryLAMMPS
from atooms.trajectory.decorators import _Molecular


class Test(unittest.TestCase):

    def setUp(self):
        """
        Set up the test case by initializing the particle trajectory.
        """
        self.input_file = os.path.join(os.path.dirname(__file__),
                                       '../data/trimer_rho1.2.lammpstrj')
        self.particle_trajectory = TrajectoryLAMMPS(self.input_file)

    def test_trajectory(self):
        """
        Test the creation of the molecular trajectory from the particle trajectory.
        """
        molecular_trajectory = MolecularTrajectoryLAMMPS(self.input_file)
        self.frame_0 = molecular_trajectory[0]
        self.molecule_0 = self.frame_0.molecule[0]
        self.particle_0 = self.frame_0.particle[0]
        self.assertIsNotNone(self.molecule_0)
        self.assertIsNotNone(self.particle_0)
        molecular_trajectory.close()

    def test_decorator(self):
        MolecularTrajectory = _Molecular(TrajectoryLAMMPS)
        molecular_trajectory = MolecularTrajectory(self.input_file)
        self.assertTrue(isinstance(molecular_trajectory, TrajectoryLAMMPS))
        self.assertTrue(isinstance(molecular_trajectory, MolecularTrajectory))
        self.frame_0 = molecular_trajectory[0]
        self.molecule_0 = self.frame_0.molecule[0]
        self.particle_0 = self.frame_0.particle[0]
        self.assertIsNotNone(self.molecule_0)
        self.assertIsNotNone(self.particle_0)
        molecular_trajectory.close()

    def test_center_of_mass(self):
        """
        Test the calculation of the center of mass of the first molecule.
        """
        self.test_trajectory()  # Ensure test_trajectory runs first
        center_of_mass = self.molecule_0.center_of_mass
        self.assertAlmostEqual(center_of_mass[0], 3.129313, places=6)
        self.assertAlmostEqual(center_of_mass[1], 6.057427, places=6)
        self.assertAlmostEqual(center_of_mass[2], 4.262863, places=6)

    def test_position(self):
        """
        Test the position of the first particle in the first frame.
        """
        self.test_trajectory()  # Ensure test_trajectory runs first
        particle_0_position = self.particle_0.position
        self.assertAlmostEqual(particle_0_position[0], 2.96049, places=6)
        self.assertAlmostEqual(particle_0_position[1], 6.62826, places=6)
        self.assertAlmostEqual(particle_0_position[2], 4.19592, places=6)

    def _test_trajectory(self, cls):
        from atooms.core.utils import rmf

        with MolecularTrajectoryLAMMPS(self.input_file) as mth:
            s = mth[0]
        N_mol = len(s.molecule)
        fout = '/tmp/molecular.xyz'
        with _Molecular(cls)(fout, 'w') as mth:
            mth.write(s, 0)
        with _Molecular(cls)(fout) as mth:
            s = mth[0]
        self.assertEqual(len(s.molecule), N_mol)
        rmf(fout)

    def test_trajectory_any(self):
        from atooms.trajectory import TrajectoryXYZ, TrajectoryEXYZ, TrajectoryRam
        self._test_trajectory(TrajectoryXYZ)
        # TODO: fix warning about unclosed file, dont know why
        self._test_trajectory(TrajectoryEXYZ)
        # self._test_trajectory(TrajectoryRam)

    def test_system(self):
        """
        Test the length of the molecule list and particle list
        """
        self.test_trajectory()  # Ensure test_trajectory runs first
        self.assertEqual(len(self.frame_0.molecule), 1000)
        self.assertEqual(len(self.frame_0.particle), 3000)

    def test_unfold(self):
        import numpy
        from atooms.system import Particle, Molecule, System, Cell
        from atooms.trajectory import MolecularTrajectoryXYZ, Unfolded

        finp = '/tmp/test_molecular.xyz'
        molecule = Molecule([Particle(position=[2.9, 2.9], species=1),
                             Particle(position=[2.8, 2.8], species=2)], bond=[0, 1])
        s = System(molecule=[molecule], cell=Cell([6.0, 6.0]))
        with MolecularTrajectoryXYZ(finp, 'w') as th:
            th.write(s, 0)
            # This is like entering from the other side
            s.molecule[0].center_of_mass += numpy.array([-5.8, 0.0])
            th.write(s, 1)
        with Unfolded(MolecularTrajectoryXYZ(finp)) as th:
            self.assertEqual(th[1].molecule[0].particle[0].position[0], 3.1)
            self.assertEqual(th[1].molecule[0].particle[0].position[1], 2.9)
            self.assertAlmostEqual(th[1].molecule[0].orientation[0][0], th[0].molecule[0].orientation[0][0])
            self.assertAlmostEqual(th[1].molecule[0].orientation[0][1], th[0].molecule[0].orientation[0][1])

    def tearDown(self):
        self.particle_trajectory.close()


if __name__ == '__main__':
    unittest.main()
