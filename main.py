import os, sys
from duckProcess import *
from Q3autograder import * # Import additional scripts as needed
from Q4autograder import *
from Q5autograder import * 

def folderCreate(qNum, secNum, teamNum):
    folderName = 'S' + str(secNum) + 'T' + str(teamNum) + 'Q' + str(qNum)
    folderPath = 'AutograderOutput\\' + folderName
    testPath = folderPath + '\\ScriptOutput\\' # Output of the script that is run
    expectPath = folderPath + '\\ExpectedOutput\\' # Expected state of the output folder
    notesPath = folderPath + '\\GradeNotes\\' # Location of csv files containing any issues with the script
    if not os.path.exists(folderPath):
        os.makedirs(folderPath, 0o777)
        os.makedirs(testPath, 0o777)
        os.makedirs(expectPath, 0o777)
        os.makedirs(notesPath, 0o777)
    else:
        print("Folders for Group and Question already found. This script may have already been graded and previous files might affect the grading process.") 
        # If folders exist already, this question may have been graded, can cause issues with grading.
        npt = input("Continue Grading? (Y/n) : ")
        if npt == 'N' or npt == 'n':
            return [True, testPath, expectPath, notesPath] # True will indicate to Q3main that folders have been found and user does not want to continue
        if not os.path.exists(testPath): # Makes test, expect, and notes folders if not already made
            os.makedirs(testPath, 0o777)
        if not os.path.exists(expectPath):
            os.makedirs(expectPath, 0o777)
        if not os.path.exists(notesPath):
            os.makedirs(notesPath, 0o777)
    return [False, testPath, expectPath, notesPath] # False indicates that new folders have been made successfully


def gradeMain(filepath, qNum, sNum, tNum, addiArg):
    print("Initializing folders...")
    folderResult = folderCreate(qNum, sNum, tNum)
    if folderResult[0]:
        return False
    if qNum == '3': # Add onto here if more questions are added
        Q3main(filepath, folderResult[1], folderResult[2], folderResult[3], addiArg)
    if qNum == '4':
        Q4main(filepath, folderResult[1], folderResult[2], folderResult[3], addiArg)
    if qNum == '5':
        Q5main(filepath, folderResult[1], folderResult[2], folderResult[3], addiArg)
    
if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description='Testing out the main.')

    #args = parser.parse_args()
    if not os.path.exists('AutograderOutput'):
        os.makedirs('AutograderOutput')
    if ((len(sys.argv) == 2) and (sys.argv[1] == 'help')):
        print("Expected Use: python3 main.py [qNum] [secNum] [teamNum] \"[filePath]\" \"[additional arguments]\"")
        print("[qNum] = Number of Question\n[secNum] = Section Number of Group\n[teamNum] = Team Number of Group\n\"[filePath]\" = Path to File, in quotes\n\"[additional arguments]\" = additional requirements for each question, in quotes")
        print("For Questions 3 and 4, include Name(s) of Student(s)\nFor Question 5, include Path to Q1C.py")
    elif (len(sys.argv) < 6):
        print("Expected Use: python3 main.py [qNum] [secNum] [teamNum] \"[filePath]\" \"[additional arguments]\"")
        print("Use \"python3 main.py help\" for more details.")
    else:
        qNum = sys.argv[1]        
        if qNum != '3' and qNum != '4' and qNum != '5': # Add onto here if more questions are added. 
            print('Question not included in AutoGrader.')
        else:
            filePath = sys.argv[4]
            valid = ValidateCode(filePath)

            npt = 'Y'
            if not valid:
                npt = input("Script is not valid, attempt grading anyway? (Y/n) : ")
            if npt == "Y" or npt == "y":
                sNum = sys.argv[2]
                tNum = sys.argv[3]
                addiArg = sys.argv[5]
                gradeMain(filePath, qNum, sNum, tNum, addiArg)
