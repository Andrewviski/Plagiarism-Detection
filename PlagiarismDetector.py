#!/usr/bin/env python3

from WordComparer import WordComparer
from InputSanitizer import clean
import sys

bad_characters = []

DEFAULT_TUPLE_SIZE = 3


# N-tuple implementation of a Plagiarism Detector
# can be inherited from if it need to be extended
class PlagiarismDetector:
    def __init__(self):
        self.string_matcher = None

    # main function that compute the plagiarism percentage
    # defaults tuple size to 3
    def get_plagiarism_percentage(self, synonyms_file, input_file1, input_file2, tuple_size=DEFAULT_TUPLE_SIZE):

        # create a new WordComparer using the specified synonyms file
        self.string_matcher = WordComparer(synonyms_file)

        words1 = []
        words2 = []

        # open input files and parse them into two lists of words
        in_file1=None
        try:
            in_file1=open(input_file1, "r")
            for line in in_file1:
                for word in line.split(" "):
                    words1.append(clean(word))
        except FileNotFoundError:
            print("first input file is invalid")
            exit(-1)
        finally:
            if not in_file1 is None:
                in_file1.close()

        in_file2 = None
        try:
            in_file2 = open(input_file2, "r")
            for line in in_file2:
                for word in line.split(" "):
                    words2.append(clean(word))
        except FileNotFoundError:
            print("second input file is invalid")
            exit(-1)
        finally:
            if not in_file2 is None:
                in_file2.close()

        # make sure tuple size is valid
        if tuple_size > len(words2) or tuple_size<1:
            print("Tuple size value is invalid!")
            exit(-1)

        # compute the percentage of matching tuples
        total_tuples = 0
        matching_tuples = 0
        for i in range(len(words1) - tuple_size + 1):
            total_tuples += 1
            if self.__KMP_Tuples(words2, words1[i:i + tuple_size]):
                matching_tuples += 1

        return (matching_tuples * 100.0) / total_tuples

    # an implementation of the prefix function pre-computation needed for KMP algorithm
    # More info: https://stackoverflow.com/questions/6594072/kmps-failure-function

    def __compute_failure(self, substring):
        # an array to store function value
        failure = [0 for i in range(len(substring))]

        # a pointer to store the last unmatched character in the substring
        k = 0

        # BaseCase= failure[0]=0
        # compute for 1...(len-1)
        for i in range(1, len(substring)):

            # use failure function to go back if words are not matching
            while k > 0 and not self.string_matcher.is_same(substring[i], substring[k]):
                k = failure[k - 1]

            # if words are matching, move to the next word
            if self.string_matcher.is_same(substring[i], substring[k]):
                k += 1

            failure[i] = k

        return failure

    # KMP algorithm for string matching used to find a matching between
    # tuple_array and sub_tuple_array
    # instead of normal character comparision we compare two lists of strings
    # using the custom string matcher built from synonyms file
    def __KMP_Tuples(self, tuple_array, sub_tuple_array):

        # precompute failure function
        failure_function = self.__compute_failure(sub_tuple_array)

        # a pointer to store the last unmatched character in the substring
        k = 0

        # try to match sub_tuple_array on positions 0...(len-1) of tuple_array
        for i in range(len(tuple_array)):

            # use failure function to go back if words are not matching
            while k > 0 and not self.string_matcher.is_same(tuple_array[i], sub_tuple_array[k]):
                k = failure_function[k - 1]

            # if words are matching, move to the next word
            if self.string_matcher.is_same(tuple_array[i], sub_tuple_array[k]):
                k += 1

            # sub_tuple_array have been fully matched
            if k == len(sub_tuple_array):
                return True
        return False


# main starting point
if __name__ == "__main__":

    if sys.version_info[0] < 3:
        print("This program requires python 3.5.2\n")
        exit(-1)

    # make sure arguments are valid
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: <synonyms_file> <base_file> <comparison_file> [<tuple_size>]")
        exit(-1)
    else:

        syn_name = sys.argv[1]
        f1_name = sys.argv[2]
        f2_name = sys.argv[3]

        if len(sys.argv) == 5:
            try:
                tuple_size = int(sys.argv[4])
            except TypeError:
                print("Fourth argument should be a number, terminating...!")
                exit(-1)
            print("Plagiarism Percentage %f%%" % PlagiarismDetector().get_plagiarism_percentage(syn_name, f1_name, f2_name, tuple_size))
        else:
            print("Plagiarism Percentage %f%%" % PlagiarismDetector().get_plagiarism_percentage(syn_name, f1_name, f2_name))
