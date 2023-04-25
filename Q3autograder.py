import os, filecmp, time, csv
from duckProcess import *

    
def Q3expectOutput(names, expectPath):
    path = expectPath + "Q3Script.bat"
    f = open(path, "x")
    fText = "echo " + names
    f.write(fText)
    f.close() 

def Q3compareAndSave(testPath, expectPath, notesPath): # Currently only compares
    testDir = os.listdir(testPath) # Only doing listdir since we already know the output of the expected output folder. Script might create extra files we don't know about
    issues = 0
    batFlag = False
    csvpath = notesPath + "gradenotes.csv"
    with open(csvpath, 'w') as file:
        csvfile = csv.writer(file)
        for f in testDir:
            if f.endswith(".bat"):
                if batFlag:
                    print("Unexpected Output: Multple .bat files created.")
                    csvfile.writerow(['Unexpected Output: Multple .bat files created.'])
                    issues += 1
                    continue
                batPath = expectPath + "Q3Script.bat"
                testBatPath = testPath + f
                if not filecmp.cmp(testBatPath, batPath):
                    print("Comparison Error: .bat file does not match expected .bat file.")
                    csvfile.writerow(['Comparison Error: .bat file does not match expected .bat file.'])
                    issues += 1
                batFlag = True
            else:
                print("Unexpected Output: Script has created a file which is not .bat.")
                csvfile.writerow(['Unexpected Output: Script has created a file which is not .bat.'])
                issues += 1
        if not batFlag:
            print("Unexpected Output: .bat file not found.")
            csvfile.writerow(['Unexpected Output: .bat file not found.'])
            issues += 1
        csvfile.writerow(['Total # of issues: ' + str(issues)])
        print("Total # of issues: " + str(issues))

def Q3main(filepath, testPath, expectPath, notesPath, names):
    Q3expectOutput(names, expectPath) 
    print("Executing Script...")
    ReadFile(filepath) # Runs file using emulator
    time.sleep(1)
    Q3compareAndSave(testPath, expectPath, notesPath)


# Testing
if __name__ == "__main__":
    if not os.path.exists("Q3Testing"):
        os.makedirs("Q3Testing", 0o777)
    if not os.path.exists("Q3Testing\\ExpectOutput"):
        os.makedirs("Q3Testing\\ExpectOutput")
    Q3expectOutput("Matt Fernand", "Q3Testing\\ExpectOutput\\")
    f = open("Q3Testing\\ExpectOutput\\Q3Script.bat", "r")
    line = f.read()
    if line != "echo Matt Fernand":
        print("Incorrect creation of .bat file in Expect Output")
    else:
        print("No issue with creating .bat file!")
    f.close()
    