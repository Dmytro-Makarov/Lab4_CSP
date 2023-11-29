import random


class Teacher:
    def __init__(self, name, subjectKnowledge, maxHours):
        self.name = name
        self.subjectKnowledge = subjectKnowledge
        self.maxHours = maxHours


class Group:
    def __init__(self, name, subjects, maxHours):
        self.name = name
        self.subjects = subjects
        self.maxHours = maxHours


class Timeslot:
    def __init__(self):
        self.subjectIdx = -1
        self.teacherIdx = -1
        self.groupIdx = -1


subjects = [
    "Discrete Math", "Physics", "Programming", "Chemistry", "Philosophy", "Calculus"
]

teachers = [
    Teacher("Tom", [False, True, False, False, False, True], 3),
    Teacher("Bob", [False, False, True, True, True, False], 5),
    Teacher("Mary", [True, False, False, False, True, True], 8)
]

groups = [
    Group("A", [False, False, False, False, True, False], 5),
    Group("B", [False, True, False, False, False, True], 6),
    Group("C", [True, False, False, False, False, False], 2),
    Group("D", [False, False, True, False, False, False], 2),
    Group("E", [False, False, False, True, False, False], 4)
]

numTeachers = len(teachers)
numGroups = len(groups)
numSubjects = len(subjects)
numTimeslots = 15


class Schedule:
    def __init__(self):
        self.timetable = [Timeslot() for _ in range(numTimeslots)]


class CSPSolver:
    def __init__(self):
        self.domains = []
        self.constraints = []
        self.bestSchedule = Schedule()
        self.schedule = Schedule()
        self.initialize_domains()
        self.initialize_constraints()

    def solve(self):
        self.backtracking(0)

    def print_schedule(self, schedule):
        print("Schedule:")
        for timeslotIdx, timeslot in enumerate(schedule.timetable):
            subjectIdx = timeslot.subjectIdx
            teacherIdx = timeslot.teacherIdx
            groupIdx = timeslot.groupIdx

            print(f"Timeslot: {timeslotIdx + 1}: ", end="")
            print(f"Subject: {subjects[subjectIdx]}, ", end="")
            print(f"Teacher: {teachers[teacherIdx].name}, ", end="")
            print(f"Group: {groups[groupIdx].name}")

    def initialize_domains(self):
        self.domains = [self.generate_assignment(timeslotIdx) for timeslotIdx in range(numTimeslots)]

    def generate_assignment(self, timeslotIdx):
        validAssignments = []

        for subjectIdx in range(numSubjects):
            for teacherIdx in range(numTeachers):
                for groupIdx in range(numGroups):
                    assignment = subjectIdx + numSubjects * teacherIdx + numSubjects * numTeachers * groupIdx
                    validAssignments.append(assignment)

        return validAssignments

    def is_valid_assignment(self, timeslotIdx, subjectIdx, teacherIdx, groupIdx):
        if not teachers[teacherIdx].subjectKnowledge[subjectIdx]:
            return False

        if not groups[groupIdx].subjects[subjectIdx]:
            return False

        return True

    def initialize_constraints(self):
        self.constraints.append(
            lambda schedule: self.no_teacher_overload(schedule) and self.no_group_overload(schedule))

    def no_teacher_overload(self, schedule):
        teacherHours = [0] * numTeachers
        for timeslot in schedule.timetable:
            if timeslot.teacherIdx != -1:
                teacherHours[timeslot.teacherIdx] += 1
                if teacherHours[timeslot.teacherIdx] > teachers[timeslot.teacherIdx].maxHours:
                    return False
        return True

    def no_group_overload(self, schedule):
        groupHours = [0] * numGroups
        for timeslot in schedule.timetable:
            if timeslot.groupIdx != -1:
                groupHours[timeslot.groupIdx] += 1
                if groupHours[timeslot.groupIdx] > groups[timeslot.groupIdx].maxHours:
                    return False
        return True

    def backtracking(self, timeslotIdx):
        if timeslotIdx == numTimeslots:
            self.bestSchedule = self.schedule
            return

        variableOrder = self.get_variable_order(timeslotIdx)

        for assignment in variableOrder:
            self.schedule.timetable[timeslotIdx].subjectIdx = assignment % numSubjects
            self.schedule.timetable[timeslotIdx].teacherIdx = (assignment // numSubjects) % numTeachers
            self.schedule.timetable[timeslotIdx].groupIdx = assignment // (numSubjects * numTeachers)

            if self.constraints_satisfied(self.schedule) and self.is_valid_assignment(timeslotIdx,
                                                                                      self.schedule.timetable[
                                                                                          timeslotIdx].subjectIdx,
                                                                                      self.schedule.timetable[
                                                                                          timeslotIdx].teacherIdx,
                                                                                      self.schedule.timetable[
                                                                                          timeslotIdx].groupIdx):
                self.backtracking(timeslotIdx + 1)

    def get_variable_order(self, timeslotIdx):
        values = self.domains[timeslotIdx]
        values.sort(key=lambda assignment: self.count_teachers_for_subject(assignment % numSubjects))
        return values

    def count_teachers_for_subject(self, subjectIdx):
        count = 0
        for teacher in teachers:
            if teacher.subjectKnowledge[subjectIdx]:
                count += 1
        return count

    def constraints_satisfied(self, schedule):
        for constraint in self.constraints:
            if not constraint(schedule):
                return False
        return True


csp = CSPSolver()
csp.solve()
csp.print_schedule(csp.bestSchedule)
