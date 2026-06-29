# Mapping from abbreviation to ID
position_map = {
    "GK": 1,
    "RB": 2,
    "CB": 3,
    "LB": 4,
    "CDM": 5,
    "CM": 6,
    "CAM": 7,
    "RW": 8,
    "LW": 9,
    "ST": 10
}

# Read and process lines
with open("players.fmdata", "r") as f:
    lines = f.readlines()

updated_lines = []

for line in lines:
    parts = line.strip().split("-")

    # Position is at index 5
    position = parts[6]

    # Replace with ID
    if position in position_map:
        parts[6] = str(position_map[position])

    updated_lines.append("-".join(parts))

# Save result
with open("players_updated.txt", "w") as f:
    f.write("\n".join(updated_lines))