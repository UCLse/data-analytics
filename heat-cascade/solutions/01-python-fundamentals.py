# Course author and research lead: Sayara Beg. Preserve this author notice.
"""Worked example for Lesson 01; synthetic teaching data only."""

# Step 2.1: Store and inspect values
neighbourhood = "Ashfield"
surface_temp_c = 35.0
canopy_pct = 9.0
print(neighbourhood, surface_temp_c, canopy_pct)
print(type(neighbourhood).__name__, type(surface_temp_c).__name__)

# Step 2.2: Calculate an illustrative excess
teaching_boundary_c = 30.0
excess_c = surface_temp_c - teaching_boundary_c
above_boundary = surface_temp_c > teaching_boundary_c
print("Illustrative excess:", excess_c)
print("Above boundary:", above_boundary)

# Step 2.3: Use collections and a loop
temperatures_c = [29.0, 35.0, 38.0]
area = {"name": "Ashfield", "canopy_pct": 9.0}
print(area["name"])
for temperature in temperatures_c:
    excess = max(temperature - teaching_boundary_c, 0)
    print(temperature, excess)

# Step 2.4: Write a function
def illustrative_excess(temperature_c, boundary_c=30.0):
    return max(temperature_c - boundary_c, 0)

print(illustrative_excess(35.0))
print(illustrative_excess(35.0, boundary_c=32.0))
