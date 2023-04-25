import os, shutil, filecmp, time, csv
from duckProcess import *

def Q5expectOutput(q1cPath, expectPath):
    newq1cPath = expectPath + "Q1C.py"
    f = open(newq1cPath, "x")
    shutil.copy(q1cPath, newq1cPath)
    f.close()
    q5aPath = expectPath + "Q5A.py" # Creates two empty python files to test if the script can infect multiple files
    f2 = open(q5aPath, "x")
    f2.close()
    q5bPath = expectPath + "Q5B.py"
    f3 = open(q5bPath, "x")
    f3.close()
    curdir = os.getcwd()
    os.chdir(expectPath) # Change working directory to the expected output folder path so that it runs on the files there
    time.sleep(0.5)
    exec(open("./Q1C.py").read()) # Runs Q1C.py one time to test infection, can't use newq1cPath as that is path from higher directory
    time.sleep(0.5) # Wait a bit to ensure script is executed completely
    os.chdir(curdir) # Return to original file location once finished
    q1cout = expectPath + "Q1C.out" # Q1C.out will have to be rewritten to match the expected output of the script
    if os.path.exists(q1cout):
        f4 = open(q1cout, "w")
        f4.write("Q1C.py, ")
        f4.close()

def Q5testInit(testPath):
    q5aPath = testPath + "Q5A.py"
    f = open(q5aPath, "x")
    f.close()
    q5bPath = testPath + "Q5B.py"
    f2 = open(q5bPath, "x")
    f2.close()

def Q5InfectionCheck(testPath, expectPath, notesPath):
    csvpath = notesPath + "gradenotes.csv"
    issues = 0
    with open(csvpath, 'a') as file:
        csvfile = csv.writer(file)
        expectq5a = expectPath + "Q5A.py"
        testq5a = testPath + "Q5A.py"
        if filecmp.cmp(expectq5a, testq5a):
            print("Q5A.py not infected during initialization.")
            csvfile.writerow(['Q5A.py not infected during initialization.'])
            issues += 1
        expectq5b = expectPath + "Q5B.py"
        testq5b = testPath + "Q5B.py"
        if filecmp.cmp(expectq5b, testq5b):
            print("Q5B.py not infected during initialization.")
            csvfile.writerow(['Q5B.py not infected during initialization.'])
            issues += 1
        expectq1cout = expectPath + "Q1C.out"
        if not os.path.exists(expectq1cout):
            print("Q1C.out does not exist, error with spyware functionality.")
            csvfile.writerow(['Q1C.out does not exist, error with spyware functionality.'])
            issues += 1
        if issues > 0:
            print("Total # of issues during initialization: " + str(issues))
        csvfile.writerow(['Total # of issues during initialization: ' + str(issues)])


def Q5compareAndSave(testPath, expectPath, notesPath, secInfect = False):
    testDir = os.listdir(testPath) # Only doing listdir since we already know the output of the expected output folder. Script might create extra files we don't know about
    issues = 0
    q1cTestFile = ''
    pyflag = False
    q1coutflag = False
    csvpath = notesPath + "gradenotes.csv"
    with open(csvpath, 'a') as file:
        csvfile = csv.writer(file)
        for f in testDir:
            if f == "Q5A.py":
                exq5aPath = expectPath + "Q5A.py"
                testq5a = testPath + "Q5A.py"
                if not filecmp.cmp(testq5a, exq5aPath):
                    if secInfect:
                        print("Comparison Error: Q5A.py does not match. Error with second infection functionality or execution of script.")
                        csvfile.writerow(['Comparison Error: Q5A.py does not match. Error with second infection functionality or execution of script.'])
                        issues += 1
                    else:
                        print("Comparison Error: Q5A.py does not match. Error with infection functionality or execution of script.")
                        csvfile.writerow(['Comparison Error: Q5A.py does not match. Error with infection functionality or execution of script.'])
                        issues += 1
                else:
                    print("No issue with Q5A.py")
            elif f == "Q5B.py":
                exq5bPath = expectPath + "Q5B.py"
                testq5b = testPath + "Q5B.py"
                if not filecmp.cmp(testq5b, exq5bPath):
                    if secInfect:
                        print("Comparison Error: Q5B.py does not match. Error with second infection functionality or execution of script.")
                        csvfile.writerow(['Comparison Error: Q5B.py does not match. Error with second infection functionality or execution of script.'])
                        issues += 1
                    else:
                        print("Comparison Error: Q5B.py does not match. Error with infection functionality or execution of script.")
                        csvfile.writerow(['Comparison Error: Q5B.py does not match. Error with infection functionality or execution of script.'])
                        issues += 1
                else:
                    print("No issue with Q5B.py")
            elif f == "Q1C.out":
                expectQ1Cout = expectPath + "Q1C.out"
                testQ1Cout = testPath + "Q1C.out"
                if not filecmp.cmp(expectQ1Cout, testQ1Cout):
                    print("Comparison Error: Q1C.out does not match. Error with second infection functionality or execution of script.")
                    csvfile.writerow(['Comparison Error: Q1C.out does not match. Error with second infection functionality or execution of script.'])
                    issues += 1
                q1coutflag = True
            else: # Can't be sure what they name the py file, so use else and let grader know if there are extra files
                if f.endswith(".py"):
                    q1cTestFile = f
                    pyPath = expectPath + "Q1C.py"
                    pyTestPath = testPath + q1cTestFile
                    if not filecmp.cmp(pyTestPath, pyPath):
                        print("Comparison Error: Ducky output .py file does not match. Error with infection functionality or Q1C.py.")
                        csvfile.writerow(['Comparison Error: Ducky output .py file does not match. Error with infection functionality or Q1C.py.'])
                        issues += 1
                    else:
                        pyflag = True
                        print("No issue with the python script")
                else:
                    print("Unexpected Output: Script has created a file which is not .py.")
                    csvfile.writerow(['Unexpected Output: Script has created a file which is not .py.'])
                    issues += 1
        if not pyflag:
            print("No .py file found in ScriptOutput. Script might not save to the ScriptOutput folder.")
            csvfile.writerow(['No .py file found in ScriptOutput. Script might not save to the ScriptOutput folder.'])
            issues += 1
        if not q1coutflag:
            print("Spyware functionality not included in .py script.")     
            csvfile.writerow(['Spyware functionality not included in .py script.'])
            issues += 1       
        if secInfect:
            print("Total # of issues with second infection: ", issues)
            csvfile.writerow(['Total # of issues with second infection: ' + str(issues)])
        else:
            print("Total # of issues with first infection: ", issues)
            csvfile.writerow(['Total # of issues with first infection: ' + str(issues)])
    return q1cTestFile

def Q5main(filepath, testPath, expectPath, notesPath, q1cPath):
    Q5expectOutput(q1cPath, expectPath)
    Q5testInit(testPath)
    Q5InfectionCheck(testPath, expectPath, notesPath)
    print("Executing Script...")
    ReadFile(filepath) # Run file in emulator
    time.sleep(1) #Sleeps for just long enough for infection from script to complete
    q1cTestFile = Q5compareAndSave(testPath, expectPath, notesPath)
    print("First comparison completed. Checking for second infection.")
    # While no second infection functionality is part of Q1C.py, it is also helpful in cases where Q1C.py from the script is not run correctly. 
    curdir = os.getcwd()
    os.chdir(testPath) #Change working directory to Script Output to ensure it is run there
    exec(open(q1cTestFile).read()) #Execute second infection
    time.sleep(0.5)
    os.chdir(curdir) # Return to original file location once finished
    q1coutPath = expectPath + "Q1C.out"
    f = open(q1coutPath, "w")
    f.write("Q1C.py, main.py, ")
    f.close()
    Q5compareAndSave(testPath, expectPath, notesPath, True) 
    print("Second comparison completed.")


# Testing
if __name__ == "__main__":
    if not os.path.exists("Q5Testing"):
        os.makedirs("Q5Testing", 0o777)
    if not os.path.exists("Q5Testing\\ExpectOutput"):
        os.makedirs("Q5Testing\\ExpectOutput")
    Q5expectOutput("Q1C.py", "Q5Testing\\ExpectOutput\\")
    fq1c = "Q5Testing\\ExpectOutput\\Q1C.py"
    fq5a = open("Q5Testing\\ExpectOutput\\Q5A.py", "r")
    fq5b = open("Q5Testing\\ExpectOutput\\Q5B.py", "r")
    expectSuccess = 3
    if not filecmp.cmp("Q1C.py", fq1c):
        print("Incorrect creation of .py file in Expect Output")
        expectSuccess -= 1
    line = "#Matt Fernand\n"
    if line not in fq5a.readlines():
        print("Q1C.py did not infect Q5A.py")
        expectSuccess -= 1
    if line not in fq5b.readlines():
        print("Q1C.py did not infect Q5B.py")
        expectSuccess -= 1
    print("Files Correctly Initialized in Expect Output: " + str(expectSuccess) + "/3")
    fq5a.close()
    fq5a.close()
    if not os.path.exists("Q5Testing\\ScriptOutput"):
        os.makedirs("Q5Testing\\ScriptOutput")
    fq5a = "Q5Testing\\ScriptOutput\\Q5A.py"
    fq5b = "Q5Testing\\ScriptOutput\\Q5B.py"
    testSuccess = 2
    if os.stat(fq5a).st_size != 0:
        print("Q5A.py in Script Output not initialized successfully.")
        testSuccess -= 1
    if os.stat(fq5b).st_size != 0:
        print("Q5B.py in Script Output not initialized successfully.")
        testSuccess -= 1
    print("Files Correctly Initialized in Script Output: " + str(testSuccess) + "/2")
    