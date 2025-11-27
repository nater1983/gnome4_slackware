import re

# Read the entire file content into a string
with open("./gnome-46/GFSBUILDS.TXT", "r") as file:
    content = file.read()

# Find all "PRGNAM:" and "REQUIRED:" sections
prgnam_matches = re.findall(r"PRGNAM: ([^\n]+)", content)
required_matches = re.findall(r"REQUIRED: ([^\n]+)", content)

# Create a dictionary of package names to their dependencies
dependencies = {}
prgnam_index = 0
required_index = 0
lines = content.split("\n")

for line in lines:
    if line.startswith("PRGNAM:"):
        prgnam = line.split(":")[1].strip()
        dependencies[prgnam] = set()
        prgnam_index = line
    elif line.startswith("REQUIRED:"):
        required = line.split(":")[1].strip().split()
        dependencies[prgnam].update(required)

# Check which packages are listed as requirements in other packages
circular_dependencies = {}

for prgnam, required in dependencies.items():
    found_circular = set(required).intersection(prgnam_matches)
    if found_circular:
        circular_dependencies[prgnam] = found_circular

# Print the circular dependencies
if circular_dependencies:
    print("These are dependencies for a Slackware-current system, assume full installation.")
    print("Following Slackware tradition, all preinstalled dependencies from full installation skipped...")
    print("Circular dependencies found:")
    print("")
    for package, circulars in circular_dependencies.items():
        print(f"{package} REQUIRES: {', '.join(circulars)}") 
else:
    print("No circular dependencies found.")

