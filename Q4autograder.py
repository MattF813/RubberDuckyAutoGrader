import os, filecmp, csv
from duckProcess import *

def Q4expectOutput(names, expectPath):
    path = expectPath + "Q4script.py"
    f = open(path, "x")
    fText = "print(\"" + names + "\")"
    f.write(fText)
    f.close() 

def Q4compareAndSave(testPath, expectPath, notesPath): # Currently only compares
    testDir = os.listdir(testPath) # Only doing listdir since we already know the output of the expected output folder. Script might create extra files we don't know about
    issues = 0
    pyFlag = False
    csvpath = notesPath + "gradenotes.csv"
    with open(csvpath, 'w') as file:
        csvfile = csv.writer(file)
        for f in testDir:
            if f.endswith(".py"):
                if pyFlag:
                    print("Unexpected Output: Multple .py files created.")
                    csvfile.writerow(['Unexpected Output: Multple .py files created.'])
                    issues += 1
                    continue
                pyPath = expectPath + "Q4Script.py"
                testPyPath = testPath + f
                if not filecmp.cmp(testPyPath, pyPath):
                    print("Comparison Error: .py file does not match expected .py file.")
                    csvfile.writerow(['Comparison Error: .py file does not match expected .py file.'])
                    issues += 1
                pyFlag = True
            else:
                print("Unexpected Output: Script has created a file which is not .py.")
                csvfile.writerow(['Unexpected Output: Script has created a file which is not .py.'])
                issues += 1
        if not pyFlag:
            print("Unexpected Output: .py file not found.")
            csvfile.writerow(['Unexpected Output: .py file not found.'])
            issues += 1
        csvfile.writerow(['Total # of issues: ' + str(issues)])
        print("Total # of issues: " + str(issues))

    

def Q4main(filepath, testPath, expectPath, notesPath, names):
    Q4expectOutput(names, expectPath) 
    print("Executing Script...")
    ReadFile(filepath) # Runs file using emulator
    Q4compareAndSave(testPath, expectPath, notesPath)


# Testing
if __name__ == "__main__":
    if not os.path.exists("Q4Testing"):
        os.makedirs("Q4Testing", 0o777)
    if not os.path.exists("Q4Testing\\ExpectOutput"):
        os.makedirs("Q4Testing\\ExpectOutput")
    Q4expectOutput("Matt Fernand", "Q4Testing\\ExpectOutput\\")
    f = open("Q4Testing\\ExpectOutput\\Q4Script.py", "r")
    line = f.read()
    if line != "print(\"Matt Fernand\")":
        print("Incorrect creation of .py file in Expect Output")
    else:
        print("No issue with creating .py file!")
    f.close()    
    