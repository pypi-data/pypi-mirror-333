# Shufflemates 🎲✨
> A simple Python package for randomly grouping members while supporting fixed pairs and locked teams.

Shufflemates is a Python package that helps you shuffle a list of members into balanced groups while ensuring that some members stay together (fixed pairs) and others remain in exclusive groups (locked teams).

## 🚀 Installation
You can install **Shufflemates** via `pip`:
```sh
pip install shufflemates
```

## 🎯 Features
- Randomly shuffle members into groups of a specified size.
- Ensure fixed pairs or teams are always grouped together.
- Lock specific groups so that no extra members are added.
- Ensure balanced team sizes even when the total number of members is not a perfect multiple of the group size.

## 🛠️ Usage
Here's a quick example of how to use Shufflemates:

```python
from shufflemates import shuffle_groups
members = list(range(17))  # Members 0 to 16

group_size = 3
fixed_pairs = [(3, 4), (7, 8, 9)]
locked_teams = [(11, 12, 13)]

# case 1
groups = shuffle_groups(members, group_size, fixed_pairs=fixed_pairs, locked_teams=locked_teams)

for idx, group in enumerate(groups, 1):
    print(f"Group {idx}: {group}")

# or 
# case 2
print_shuffle_group(
    members,
    group_size,
    fixed_pairs=fixed_pairs,
    locked_teams=locked_teams,
    num_iterations=12,
    iterations_time=0.5)
```

## ✅ Example Output
```sql
Group 1: [3, 4, 1]
Group 2: [7, 8, 9]
Group 3: [11, 12, 13]  <-- Locked team (No extra members)
Group 4: [2, 10, 14]
Group 5: [15, 0, 6]
Group 6: [5, 16]
```
 
## 📜 License
This project is licensed under the MIT License.

