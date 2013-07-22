import time
from webParser import WebParser
from matcher import Matcher
from profParser import RateMyProfParser


# default values left for debugging
sessionString = "fall 2013"
# userCourses = ["math 135", "math 137", "cs 145", "afm 101", "econ 101"]
userCourses = []
courses = []
generator = None
myTime = time.time()


def programTime():
    print "This program took {:.2f}s to complete.".format(time.time()
                                                          - myTime)


def getUserInfo(userCourses):
    print "Hello! I am Classy, and I'll optimize your course selection."
    print "The current optimizations are:"
    print "1.\tno time conflicts."
    print "2.\tsorting by ratemyprofessor.com ratings.\n"

    sessionString = raw_input("Which session you are in? (e.g. 'fall 2013'"
                              " without quotes): ")
    print

    cour = ""
    while cour.strip() != "0":
        print "Please add a(nother) course (e.g. 'math 145')."
        cour = raw_input("Enter '0' to stop adding: ")
        userCourses.append(cour.strip().upper())
        print
    userCourses.pop()  # the last '0'


def queryUniversity(userCourses, courses):
    print "Currently querying adm.uwaterloo.ca..."
    for courseName in userCourses:
        tmp = WebParser(courseName, sessionString).run()
        courses.append(tmp)
    print "Done!\n"


def queryRateMyProfessors(courses):
    print "Currently querying ratemyprofessors.com..."

    for i, course in enumerate(courses):
        print "Process: Course {}/{}".format(str(i+1), len(courses))

        for j, slot in enumerate(course.lectures):
            #print "Lecture {}/{}".format(str(j+1), len(course.lectures))
            ret = RateMyProfParser(slot.instructor).getInfo()
            if ret:
                slot.numRatings, slot.quality, slot.easiness = ret

        for j, slot in enumerate(course.tutorials):
            #print "Tutorial {}/{}".format(str(j+1), len(course.tutorials))
            ret = RateMyProfParser(slot.instructor).getInfo()
            if ret:
                slot.numRatings, slot.quality, slot.easiness = ret
    print "Done!\n"


def postProcessing(courses):
    # sort by ease, then quality, then number of ratings
    for course in courses:
        course.lectures.sort(key=lambda x: (x.easiness, x.quality,
                                            x.numRatings), reverse=True)
        course.tutorials.sort(key=lambda x: (x.easiness, x.quality,
                                             x.numRatings), reverse=True)


def scheduleGeneration(generator):
    print "All calculations complete!"
    print "You will be given a chance to save your selected schedule" \
          " later."
    print "Format is: "
    attrs = ["Class #", "CompSec", "Location", "Start", "End", "Days",
             "Building", "Room", "Instructor"]
    for i in attrs:
        print i,
    print

    generator = Matcher(courses).matching()

    for schedule in generator:
        for slot in schedule:
            print slot
        print
        inp = raw_input("enter 's' to save the last schedule to a file;"
                        " enter 'n' to see another possible schedule: ")
        if inp.lower() == 's':
            break

    print "Sorry! No more schedules left! :(\n"
    outputFile = raw_input("\nWhere would you like to save this schedule?"
                           " Please enter a file name: ")
    f = open(outputFile+".txt", "w")
    for slot in schedule:
        f.write(str(slot) + "\n")
    f.close()

    print "\nOkay! The file is saved at {}. Have a nice" \
          " day.".format(outputFile+".txt")


getUserInfo(userCourses)
queryUniversity(userCourses, courses)
queryRateMyProfessors(courses)
postProcessing(courses)
# programTime()
scheduleGeneration(generator)
