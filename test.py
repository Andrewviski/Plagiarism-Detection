#!/usr/bin/env python3

from PlagiarismDetector import PlagiarismDetector

f1_name = "f1.txt"
f2_name = "f2.txt"
syn_name = "synonyms.txt"

if __name__ == "__main__":

    print("Creating dummy synonyms file (synonyms.txt)...")
    syn = open(syn_name, "w")
    syn.writelines(["jog run\n", "lol haha\n", "what huh\n"])
    syn.close()

    print("Creating dummy input files (f1.txt,f2.txt)...")
    f1 = open(f1_name, "w")
    f1.write("let'S Go to jog test what")
    f1.close()

    f2 = open(f2_name, "w")
    f2.write("Let's go to run huh")
    f2.close()

    detector = PlagiarismDetector()

    for i in range(1,6):
        print("Plagiarism Percentage %f%% for tuple size= %d" % (detector.get_plagiarism_percentage(syn_name,f1_name, f2_name, i),i))
    print("Plagiarism Percentage %f%% with default tuple size" %
    detector.get_plagiarism_percentage(syn_name,f1_name, f2_name))

