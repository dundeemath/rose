from pulp import LpMaximize, LpProblem, LpVariable, lpSum
import math
import csv

# Room areas in square meters
rooms = {
    "Room_5005_a": 31.43,
    "Room_5005_b": 153.65,
    "Room_5005_c": 59.36,
    "Room_5005_d": 62.86,
    "Room_5009_a": 65.2,
    "Room_5033_a": 13.33,
    "Room_5033_b": 73.07,
    # "Room_5033A_a": 2.58,
    "Room_5033A_b": 14.12,
    "Room_5035_a": 13.07,
    "Room_5035_b": 71.63,
    "Room_6009_a": 104.5,
    "Room_6013_a": 32.3,
    "Room_6014_a": 25.0,
    "Room_6022_a": 151.5,
    "Room_6023_a": 16.6,
    "Room_6032_a": 207.6,
    "Room_6035_a": 313.6,
    "Room_7019_a": 26.0,
    "Room_7029_a": 62.26,
    "Room_7029_b": 62.26,
    "Room_7034_a": 50.12,
    "Room_7034_b": 106.78,
    "Room_7038_a": 28.5,
    "Room_7038_b": 28.5,
    "Room_7038_c": 57.0,
    "Room_8006_a": 80.6,
    "Room_8006_b": 171.7,
    "Room_8010_a": 229.0,
    "Room_8011_a": 171.0,
    "Room_8022_a": 92.0
}

b = 1.0
# Student types with `size` (space requirements  in square meters), `value` (per student in £), `max_count` & `min_count` (counts), `occupancy` (between 0 and 1)
student_types = {
    "Student_A": {"size": 3.0, "value": 8931.0, "min_count": 1, "max_count": math.floor(b*152), "occupancy": 0.60}, 
    "Student_B": {"size": 3.0, "value": 8931.0, "min_count": 1, "max_count": math.floor(b*11), "occupancy": 0.55},
    # "Student_C": {"size": 4.1, "value": 6873.0, "min_count": 1, "max_count": math.floor(b*333), "occupancy": 0.80},
    # "Student_D": {"size": 5.5, "value": 0.0, "min_count": 0, "max_count": 0},
    "Student_E": {"size": 5.5, "value": 5601.0, "min_count": 1, "max_count": math.floor(b*37), "occupancy": 1.00},
    # "Student_F": {"size": 5.5, "value": 0.0, "min_count": 0, "max_count": 0},
    # "Student_G": {"size": 3.2, "value": 0.0, "min_count": 0, "max_count": 0},
    # "Student_H": {"size": 3.0, "value": 0.0, "min_count": 0, "max_count": 0},
    # "Student_I": {"size": 3.0, "value": 0.0, "min_count": 0, "max_count": 0},
    "Student_J": {"size": 4.1, "value": 5601.0, "min_count": 1, "max_count": math.floor(b*28), "occupancy": 0.70},
    # "Student_K": {"size": 5.5, "value": 0.0, "min_count": 0, "max_count": 0},
    "Student_L": {"size": 5.5, "value": 8931.0, "min_count": 1, "max_count": math.floor(b*373), "occupancy": 1.00},
    # "Student_M": {"size": 5.5, "value": 0.0, "min_count": 0, "max_count": 0},
    "Student_N": {"size": 3.7, "value": 8931.0, "min_count": 1, "max_count": math.floor(b*250), "occupancy": 1.00},
    "Student_O": {"size": 3.2, "value": 8931.0, "min_count": 1, "max_count": math.floor(b*103), "occupancy": 0.65},
    # "Student_P": {"size": 3.2, "value": 0.0, "min_count": 0, "max_count": 0},
    "Student_Q": {"size": 4.1, "value": 6873.0, "min_count": 1, "max_count": math.floor(b*60), "occupancy": 1.00},
    "Student_R": {"size": 3.0, "value": 8931.0, "min_count": 1, "max_count": math.floor(b*43), "occupancy": 0.60},
    "Student_S": {"size": 5.5, "value": 8931.0, "min_count": 1, "max_count": math.floor(b*20), "occupancy": 1.00},
    "Student_T": {"size": 5.5, "value": 8931.0, "min_count": 1, "max_count": math.floor(b*20), "occupancy": 0.55},
    # "Student_U": {"size": 3.7, "value": 0.0, "min_count": 0, "max_count": 0},
    "Student_V": {"size": 3.2, "value": 8931.0, "min_count": 1, "max_count": math.floor(b*81), "occupancy": 1.00},
    "Student_W": {"size": 3.0, "value": 6873.0, "min_count": 1, "max_count": math.floor(b*53), "occupancy": 1.00}
}



# Define the optimization problem
model = LpProblem("Room_Packing", LpMaximize)

# Decision variables
y = { (s, r): LpVariable(f"y_{s}_{r}", lowBound=0, cat='Integer') for s in student_types for r in rooms }
z = { (s, r): LpVariable(f"z_{s}_{r}", cat='Binary') for s in student_types for r in rooms }

# Objective function
model += lpSum(student_types[s]["value"] * y[s, r] for s in student_types for r in rooms), "Total_Value"

# Constraints
for r in rooms:
    model += lpSum((student_types[s]["size"] * student_types[s]["occupancy"]) * y[s, r] for s in student_types) <= rooms[r], f"Scaled_Area_Constraint_{r}"
    model += lpSum(z[s, r] for s in student_types) <= 1, f"One_Student_Type_Per_Room_{r}"
    for s in student_types:
        model += (student_types[s]["size"] * student_types[s]["occupancy"]) * y[s, r] <= z[s, r] * rooms[r], f"Student_Type_Selection_Constraint_{s}_{r}"

for s in student_types:
    model += lpSum(y[s, r] for r in rooms) >= student_types[s]["min_count"], f"Min_Count_{s}"
    model += lpSum(y[s, r] for r in rooms) <= student_types[s]["max_count"], f"Max_Count_{s}"

# Solve the model
model.solve()

# Define the output file path
output_file_path = "opt_packing.txt"
# Open the file for writing
with open(output_file_path, "w") as file:
    # Write the results to the file
    file.write("### Optimal packing plan (by student type by room) ###\n")
    for s in student_types:
        for r in rooms:
            if y[s, r].value() > 0:
                file.write(f"\t{s} in \t{r}: \t{int(y[s, r].value())} \tunits\n")
    
    file.write(f"\nTotal stored value: {model.objective.value()}\n")
    
    file.write("\n### Optimal packing plan (by room) ###\n")
    for r in rooms:
        for s in student_types:
            if y[s, r].value() > 0:
                file.write(f"\tFill {r} with \t{int(y[s, r].value())} units of \t{s}\n")
    
    file.write(f"\nTotal stored value: {model.objective.value()}\n")
    
    # Append the Room and Student data
    file.write("\n### Room Data Used ###")
    file.write("\nType \t\tsize (m²)\n")
    for room, area in rooms.items():
        file.write(f"{room}: \t{area}\n")
    
    file.write("\n### Student Data Used ###")
    file.write("\nType \t\tsize (m²) \tvalue (£) \tmin \tmax\n")
    for student, data in student_types.items():
        file.write(f"{student}\t{data['size']}\t\t\t{data['value']}\t\t{data['min_count']}\t{data['max_count']}\n")
  
# Save results to CSV
with open("opt_packing.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Student Type", "Room", "Room Size (m*m)", "Units Assigned", "Total Student Space (m*m)", "Desired Occupancy", "Calculated Occupancy", "Value in Room (GBP))"])
    for s in student_types:
        for r in rooms:
            if y[s, r].value() > 0:
                units_assigned = int(y[s, r].value())
                room_size = rooms[r]  # The size of the room
                total_student_space = units_assigned * student_types[s]["size"]  # Total space used by this student type
                calculated_occupancy = room_size / total_student_space if total_student_space > 0 else 0  # Avoid division by zero
                desired_occupancy = student_types[s]["occupancy"]
                value_stored = units_assigned * student_types[s]["value"]  # Compute total stored value
                writer.writerow([s, r, room_size, units_assigned, total_student_space, desired_occupancy, calculated_occupancy, value_stored])


with open("oom_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Room", "Size (m*m)"])
    for room, area in rooms.items():
        writer.writerow([room, area])

with open("student_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Student Type", "Size (m*m)", "Value (GBP)", "Min Count", "Max Count", "Occupancy"])
    for student, data in student_types.items():
        writer.writerow([student, data["size"], data["value"], data["min_count"], data["max_count"], data["occupancy"]])
