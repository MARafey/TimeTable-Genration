import random
Batch_21 = ["Information Security","Professional Paractices"]
Batch_22 = ["'Automata","SDA","Stat Modeling","C net","TBW"]
Batch_23 = ["Dicrete Mathematics","Data Structures","Computer Assemly","Linear Algebra"]
Batch_24 = ["Programming Fundamentals","Applied Physics","Calculas","English","Islamiat"]

Total_Classes_Per_Batch = 5

Electives = ["Fundamentals of Marketing","Marketing Managment","Pycology","Web","SMD","DIP","Advanced Programming","Data Science","Machine Learning","AI","IOT","Cloud Computing","Cyber Security","Network Security"]

Sections_Names = []
Total_Sections = 5
for i in range (Total_Sections):
    Sections_Names.append("Section "+str(i+1))

Total_Floors = 5
Class_Rooms_Per_Floor = 10
Class_Rooms = []
for i in range (Total_Floors):
    for j in range (Class_Rooms_Per_Floor):
        Class_Rooms.append("Floor "+str(i+1)+" Room "+str(j+1))


Lab_Rooms_Per_Floor = 3
Lab_Rooms = []
for i in range (Total_Floors):
    for j in range (Lab_Rooms_Per_Floor):
        Lab_Rooms.append("Floor "+str(i+1)+" Lab "+str(j+1))

Teacher = []
Total_Teachers = 15
for i in range (Total_Teachers):
    Teacher.append("Teacher "+str(i+1))


from datetime import datetime, timedelta

Number_of_Classes_one_Teacher_can_take = 3
Time_Slots = []
Start_Time = datetime.strptime("08:30", "%H:%M")
break_time = timedelta(minutes=15) #minutes
Class_Interval = timedelta(minutes=80) #minutes == 1 hour 20 minutes
Total_Classes_Per_day = 7
for i in range(Total_Classes_Per_day):
    Time_Slots.append(Start_Time.strftime("%H:%M"))
    Start_Time = Start_Time + Class_Interval + break_time
    if i == (Total_Classes_Per_day-2):
        Start_Time -= break_time

Capacity_of_Class_Rooms = []
for i in range(len(Class_Rooms)):
    Capacity_of_Class_Rooms.append(60)

# Randomly making some class rooms with capacity of 120
for i in range(10):
    Capacity_of_Class_Rooms[random.randint(0,len(Class_Rooms)-1)] = 120


Days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]

'''
# printing all the data
print("Batch_21: ",Batch_21)
print("Batch_22: ",Batch_22)
print("Batch_23: ",Batch_23)
print("Batch_24: ",Batch_24)
print("Total_Classes_Per_Batch: ",Total_Classes_Per_Batch)
print("Electives: ",Electives)
print("Sections_Names: ",Sections_Names)
print("Total_Sections: ",Total_Sections)
print("Total_Floors: ",Total_Floors)
print("Class_Rooms_Per_Floor: ",Class_Rooms_Per_Floor)
print("Class_Rooms: ",Class_Rooms)
print("Lab_Rooms_Per_Floor: ",Lab_Rooms_Per_Floor)
print("Lab_Rooms: ",Lab_Rooms)
print("Teacher: ",Teacher)
print("Total_Teachers: ",Total_Teachers)
print("Number_of_Classes_one_Teacher_can_take: ",Number_of_Classes_one_Teacher_can_take)
print("Time_Slots: ",Time_Slots)
print("Total_Classes_Per_day: ",Total_Classes_Per_day)
print("Capacity_of_Class_Rooms: ",Capacity_of_Class_Rooms)
print("Days: ",Days)
'''

# creating a random timetable for a week
def create_random_timetable():
    timetable = {}
    # for each day there will be a timetable
    # each time slot will have a class or lab in each class room
    # each class will have a teacher and a section and a course which will be randomly selected
    for day in Days:
        timetable[day] = {}
        for time_slot in Time_Slots:
            timetable[day][time_slot] = {}
            for class_room in Class_Rooms:
                timetable[day][time_slot][class_room] = {}
                timetable[day][time_slot][class_room]["class"] = {}
                timetable[day][time_slot][class_room]["class"]["teacher"] = random.choice(Teacher)
                timetable[day][time_slot][class_room]["class"]["section"] = random.choice(Sections_Names)
                timetable[day][time_slot][class_room]["class"]["course"] = random.choice(Batch_21 + Batch_22 + Batch_23 + Batch_24 + Electives)
                timetable[day][time_slot][class_room]["class"]["class_type"] = random.choice(["Theory","Lab"])
                timetable[day][time_slot][class_room]["class"]["class_room_capacity"] = Capacity_of_Class_Rooms[Class_Rooms.index(class_room)]
    return timetable

def BinaryEncoding(TimeTable):
    encoded_timetable = []
    for day in Days:
        for time_slot in Time_Slots:
            for class_room in Class_Rooms:
                class_details = TimeTable[day][time_slot][class_room]["class"]
                course = class_details["course"]
                class_type = class_details["class_type"]
                section = class_details["section"]
                professor = class_details["teacher"]
                class_room_capacity = class_details["class_room_capacity"]
                encoded_class = [course, class_type, section, professor, day, time_slot, class_room, class_room_capacity]
                encoded_timetable.append(encoded_class)
    return encoded_timetable

def Fitness(Encoded_Timetable):
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
    # Soft Constraints:
    # All the theory classes should be taught in the morning session and all the lab sessions should be done in the afternoon session.
    # Teachers/students may be facilitated by minimizing the number of floors they have to traverse. That is, as much as possible, scheduled classes should be on the same floor for either party.
    # A class should be held in the same classroom across the whole week.
    # Teachers may prefer longer blocks of continuous teaching time to minimize interruptions and maximize productivity except when the courses are different.

    FitnessValue = 0
    # Checking Hard Constraints
    # Classes can only be scheduled in free classrooms.

    for encoded_class in Encoded_Timetable:
        if encoded_class[6] not in Class_Rooms:
            FitnessValue += 1
    # A classroom should be big enough to accommodate the section. There should be two categories of classrooms: classroom (60) and large hall (120).
    for encoded_class in Encoded_Timetable:
        if encoded_class[6] in Class_Rooms:
            if encoded_class[7] == 60:
                if encoded_class[2] in Sections_Names:
                    FitnessValue += 1
            elif encoded_class[7] == 120:
                if encoded_class[2] in Sections_Names:
                    FitnessValue += 1
    # A professor should not be assigned two different lectures at the same time.
    for encoded_class in Encoded_Timetable:
        for other_encoded_class in Encoded_Timetable:
            if encoded_class != other_encoded_class:
                if encoded_class[3] == other_encoded_class[3]:
                    if encoded_class[4] == other_encoded_class[4]:
                        FitnessValue += 1
    # The same section cannot be assigned to two different rooms at the same time.
    for encoded_class in Encoded_Timetable:
        for other_encoded_class in Encoded_Timetable:
            if encoded_class != other_encoded_class:
                if encoded_class[2] == other_encoded_class[2]:
                    if encoded_class[4] == other_encoded_class[4]:
                        FitnessValue += 1
    # A room cannot be assigned for two different sections at the same time.
    for encoded_class in Encoded_Timetable:
        for other_encoded_class in Encoded_Timetable:
            if encoded_class != other_encoded_class:
                if encoded_class[6] == other_encoded_class[6]:
                    if encoded_class[4] == other_encoded_class[4]:
                        FitnessValue += 1
    # No professor can teach more than 3 courses.
    for teacher in Teacher:
        count = 0
        for encoded_class in Encoded_Timetable:
            if encoded_class[3] == teacher:
                count += 1
        if count > 3:
            FitnessValue += 1
    # No section can have more than 5 courses in a semester.
    for section in Sections_Names:
        count = 0
        for encoded_class in Encoded_Timetable:
            if encoded_class[2] == section:
                count += 1
        if count > 5:
            FitnessValue += 1
    # Each course would have two lectures per week not on the same or adjacent days.
    for course in Batch_21 + Batch_22 + Batch_23 + Batch_24 + Electives:
        count = 0
        for encoded_class in Encoded_Timetable:
            if encoded_class[0] == course:
                count += 1
        if count != 2:
            FitnessValue += 1
    # Lab lectures should be conducted in two consecutive slots.
    for encoded_class in Encoded_Timetable:
        if encoded_class[1] == "Lab":
            if encoded_class[5] != Time_Slots[-1]:
                if [encoded_class[4],Time_Slots[Time_Slots.index(encoded_class[5])+1],encoded_class[6]] not in Encoded_Timetable:
                    FitnessValue += 1
    # Checking Soft Constraints
    # All the theory classes should be taught in the morning session and all the lab sessions should be done in the afternoon session.
    for encoded_class in Encoded_Timetable:
        if encoded_class[1] == "Theory":
            if encoded_class[5] not in Time_Slots[0:4]:
                FitnessValue += 0.5
        elif encoded_class[1] == "Lab":
            if encoded_class[5] not in Time_Slots[4:]:
                FitnessValue += 0.5
    # Teachers/students may be facilitated by minimizing the number of floors they have to traverse. That is, as much as possible, scheduled classes should be on the same floor for either party.
    for encoded_class in Encoded_Timetable:
        for other_encoded_class in Encoded_Timetable:
            if encoded_class != other_encoded_class:
                if encoded_class[3] == other_encoded_class[3]:
                    if encoded_class[6][0] != other_encoded_class[6][0]:
                        FitnessValue += 0.5
    # A class should be held in the same classroom across the whole week.
    for encoded_class in Encoded_Timetable:
        for other_encoded_class in Encoded_Timetable:
            if encoded_class != other_encoded_class:
                if encoded_class[0] == other_encoded_class[0]:
                    if encoded_class[2] == other_encoded_class[2]:
                        if encoded_class[3] == other_encoded_class[3]:
                            if encoded_class[6] != other_encoded_class[6]:
                                FitnessValue += 0.5
    # Teachers may prefer longer blocks of continuous teaching time to minimize interruptions and maximize productivity except when the courses are different.
    for teacher in Teacher:
        time_slots = []
        for encoded_class in Encoded_Timetable:
            if encoded_class[3] == teacher:
                time_slots.append(encoded_class[5])
        for i in range(len(time_slots)-1):
            if Time_Slots.index(time_slots[i+1]) - Time_Slots.index(time_slots[i]) != 1:
                FitnessValue += 0.5
    # return FitnessValue
    # returning inverted value of FitnessValue
    return -FitnessValue


# printing the timetable


def Selection(Population):
    # Selecting the best 50% of the population
    Population = sorted(Population, key=lambda x: x[1], reverse=True)
    SelectedPopulation = Population[:len(Population)//2]
    return SelectedPopulation

def TwoPointCrossover(Parent1, Parent2):
    # Selecting two random points
    point1 = random.randint(0,len(Parent1)-1)
    point2 = random.randint(0,len(Parent1)-1)
    if point1 > point2:
        point1, point2 = point2, point1
    Child1 = Parent1[:point1] + Parent2[point1:point2] + Parent1[point2:]
    Child2 = Parent2[:point1] + Parent1[point1:point2] + Parent2[point2:]
    return Child1, Child2

def Mutation(Child):
    # Selects random value from child either the teacher,class,time or room and changes it to a random value
    index = random.randint(0,len(Child)-1)
    mutation_index = random.randint(0,len(Child[index])-1)
    if mutation_index == 0:
        Child[index][mutation_index] = random.choice(Batch_21 + Batch_22 + Batch_23 + Batch_24 + Electives)
    elif mutation_index == 3:
        Child[index][mutation_index] = random.choice(Teacher)
    elif mutation_index == 6:
        Child[index][mutation_index] = random.choice(Class_Rooms)
    return Child

def GeneticAlgorithm(TimeTable,iteration,mutationRate,CrossoverRate):
    Population = []
    for i in range(100):
        TimeTable = create_random_timetable()
        Encoded = BinaryEncoding(TimeTable)
        FitnessValue = Fitness(Encoded)
        Population.append([Encoded,FitnessValue])
    for i in range(iteration):
        # printing the fitness value of the best timetable in the population in each interation
        print("Iteration: ",i," Fitness: ",Population[0][1])
        SelectedPopulation = Selection(Population)
        NewPopulation = []
        while len(NewPopulation) < len(Population):
            Parent1 = random.choice(SelectedPopulation)[0]
            Parent2 = random.choice(SelectedPopulation)[0]
            if random.random() < CrossoverRate:
                Child1, Child2 = TwoPointCrossover(Parent1, Parent2)
                if random.random() < mutationRate:
                    Child1 = Mutation(Child1)
                if random.random() < mutationRate:
                    Child2 = Mutation(Child2)
                NewPopulation.append([Child1,Fitness(Child1)])
                NewPopulation.append([Child2,Fitness(Child2)])
        Population = NewPopulation
    Population = sorted(Population, key=lambda x: x[1], reverse=True)
    return Population[0]

TimeTable = create_random_timetable()
print()
print(GeneticAlgorithm(TimeTable,100,0.1,0.8))
#
# TimeTable = create_random_timetable()
# Encoded = BinaryEncoding(TimeTable)
# print(Encoded)
# print("Fitness: ",Fitness(Encoded))
