import random
from datetime import datetime, timedelta

# Data Initialization
batch_courses = {
    'Batch_21': ["Information Security", "Professional Practices"],
    'Batch_22': ["Automata", "SDA", "Stat Modeling", "C net", "TBW"],
    'Batch_23': ["Discrete Mathematics", "Data Structures", "Computer Assembly", "Linear Algebra"],
    'Batch_24': ["Programming Fundamentals", "Applied Physics", "Calculus", "English", "Islamiat"]
}

electives = ["Fundamentals of Marketing", "Marketing Management", "Psychology", "Web", "SMD", "DIP",
             "Advanced Programming", "Data Science", "Machine Learning", "AI", "IoT", "Cloud Computing",
             "Cyber Security", "Network Security"]

teachers = ["Teacher " + str(i + 1) for i in range(15)]
sections_names = ["Section " + str(i + 1) for i in range(5)]

# Room and Floor Management
total_floors = 5
rooms_per_floor = 10
labs_per_floor = 3
class_rooms = ["Floor {} Room {}".format(i+1, j+1) for i in range(total_floors) for j in range(rooms_per_floor)]
lab_rooms = ["Floor {} Lab {}".format(i+1, j+1) for i in range(total_floors) for j in range(labs_per_floor)]

# Time Slots
start_time = datetime.strptime("08:30", "%H:%M")
class_duration = timedelta(minutes=80)
break_time = timedelta(minutes=15)
time_slots = [(start_time + (class_duration + break_time) * i).strftime("%H:%M") for i in range(7)]

# Days and Capacities
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
room_capacities = [60] * len(class_rooms) + [120] * len(lab_rooms)
random.choices(room_capacities, k=10)  # Randomly assign 120 capacity to 10 rooms

# Utility Functions
def get_random_course():
    all_courses = sum(batch_courses.values(), []) + electives
    return random.choice(all_courses)

def get_random_room():
    return random.choice(class_rooms + lab_rooms)

def create_random_timetable():
    timetable = {}
    for day in days:
        for time_slot in time_slots:
            timetable[(day, time_slot)] = []
            for section in sections_names:
                course = get_random_course()
                room = get_random_room()
                teacher = random.choice(teachers)
                timetable[(day, time_slot)].append({
                    "section": section,
                    "course": course,
                    "room": room,
                    "teacher": teacher,
                    "type": "Lab" if "Lab" in room else "Theory"
                })
    return timetable

def encode_timetable(timetable):
    return [(key, value) for key, values in timetable.items() for value in values]

def calculate_fitness(timetable):
    conflicts = 0
    # Hard Constraints:
    # Classes can only be scheduled in free classrooms.
    # A classroom should be big enough to accommodate the section. There should be two categories of classrooms: classroom (60) and large hall (120).
    # A professor should not be assigned two different lectures at the same time.
    # The same section cannot be assigned to two different rooms at the same time.
    # A room cannot be assigned for two different sections at the same time.
    # No professor can teach more than 3 courses.
    # No section can have more than 5 courses in a semester.
    # Each course would have two lectures per week not on the same or adjacent days.
    # Lab lectures should be conducted in two consecutive slots.

    # implementation
    for (day, time_slot), values in timetable.items():
        for i in range(len(values)):
            for j in range(i+1, len(values)):
                if values[i]['room'] == values[j]['room']: # A room cannot be assigned for two different sections at the same time.
                    conflicts += 1
                if values[i]['teacher'] == values[j]['teacher']: # A professor should not be assigned two different lectures at the same time.
                    conflicts += 1
                if values[i]['section'] == values[j]['section']: # The same section cannot be assigned to two different rooms at the same time.
                    conflicts += 1

    for teacher in teachers:
        courses = [value['course'] for values in timetable.values() for value in values if value['teacher'] == teacher] # No professor can teach more than 3 courses.
        if len(set(courses)) > 3:
            conflicts += 1

    for section in sections_names:
        courses = [value['course'] for values in timetable.values() for value in values if value['section'] == section]
        if len(set(courses)) > 5: # No section can have more than 5 courses in a semester.
            conflicts += 1

    for section in sections_names:
        for course in sum(batch_courses.values(), []):
            count = 0
            for values in timetable.values():
                for value in values:
                    if value['section'] == section and value['course'] == course: # Each course would have two lectures per week not on the same or adjacent days.
                        count += 1
            if count > 2: # Each course would have two lectures per week not on the same or adjacent days.
                conflicts += 1
            if count < 2: # Each course would have two lectures per week not on the same or adjacent days.
                conflicts += 1

    for (day, time_slot), values in timetable.items():
        for i in range(len(values)-1):
            if values[i]['type'] == 'Lab' and values[i+1]['type'] == 'Lab': # Lab lectures should be conducted in two consecutive slots.
                conflicts += 1

    return -conflicts

def decode_timetable(encoded_timetable):
    timetable = {}
    for key, value in encoded_timetable:
        if key not in timetable:
            timetable[key] = []
        timetable[key].append(value)
    return timetable

def mutate_timetable(timetable):
    encoded_timetable = encode_timetable(timetable)
    random_index = random.randint(0, len(encoded_timetable)-1)
    key, value = encoded_timetable[random_index]
    new_value = {
        "section": value['section'],
        "course": get_random_course(),
        "room": get_random_room(),
        "teacher": random.choice(teachers),
        "type": "Lab" if "Lab" in value['room'] else "Theory"  # Corrected line
    }
    encoded_timetable[random_index] = (key, new_value)
    return decode_timetable(encoded_timetable)

def crossover_timetables(timetable1, timetable2):
    # using 2 point crossover
    encoded_timetable1 = encode_timetable(timetable1)
    encoded_timetable2 = encode_timetable(timetable2)
    random_index1 = random.randint(0, len(encoded_timetable1)-1)
    random_index2 = random.randint(random_index1, len(encoded_timetable1)-1)
    child = encoded_timetable1[:random_index1] + encoded_timetable2[random_index1:random_index2] + encoded_timetable1[random_index2:]
    return decode_timetable(child)


# Main
population_size = 10
population = [create_random_timetable() for _ in range(population_size)]
fitness_scores = [calculate_fitness(timetable) for timetable in population]
best_timetable = population[fitness_scores.index(max(fitness_scores))]
best_fitness = max(fitness_scores)
print("Initial Best Fitness:", best_fitness)

previous_best_fitness = best_fitness
for generation in range(10000):
    new_population = []
    for _ in range(population_size):
        random_index1 = random.randint(0, population_size-1)
        random_index2 = random.randint(0, population_size-1)
        child = crossover_timetables(population[random_index1], population[random_index2])
        new_population.append(mutate_timetable(child))
    population = new_population
    fitness_scores = [calculate_fitness(timetable) for timetable in population]
    new_best_fitness = max(fitness_scores)
    if new_best_fitness > best_fitness:
        best_fitness = new_best_fitness
        best_timetable = population[fitness_scores.index(best_fitness)]

    if new_best_fitness != previous_best_fitness:
        # print("Iteration ", generation, "Best Fitness:", new_best_fitness)
        previous_best_fitness = new_best_fitness


print("Final Best Fitness:", best_fitness)
print(best_timetable)
