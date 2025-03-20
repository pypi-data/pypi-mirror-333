import unittest
from shufflemates.main import shuffle_groups, print_shuffle_groups


class TestShuffleGroups(unittest.TestCase):
    def test_group_sizes(self):
        members = list(range(10))
        group_size = 3

        groups = shuffle_groups(
            members,
            group_size,
            fixed_pairs=[(0, 1)],
            locked_teams=[[2, 3]]
        )

        # Check that all members are included
        self.assertEqual(sum(len(group) for group in groups), len(members))

    def test_fixed_pairs(self):
        members = list(range(10))
        group_size = 3

        groups = shuffle_groups(members, group_size, fixed_pairs=[(0, 1)])
        for group in groups:
            if 0 in group:
                self.assertIn(1, group)
            if 1 in group:
                self.assertIn(0, group)

    def test_locked_teams(self):
        members = list(range(10))
        group_size = 3

        groups = shuffle_groups(members, group_size, locked_teams=[[0, 1]])
        for group in groups:
            if 0 in group:
                self.assertIn(1, group)
            if 1 in group:
                self.assertIn(0, group)

    def test_group_size(self):
        members = list(range(10))
        group_size = 3

        groups = shuffle_groups(members, group_size)
        for group in groups:
            self.assertLessEqual(len(group), group_size)

    def test_print_shuffle_groups(self):
        members = list(range(10))
        group_size = 3

        print_shuffle_groups(
            members,
            group_size,
            fixed_pairs=[(0, 1)],
            locked_teams=[[2, 3]],
            num_iterations=1,
            iterations_time=0,
        )


# python -m unittest tests/test_main.py
if __name__ == "__main__":
    unittest.main()
