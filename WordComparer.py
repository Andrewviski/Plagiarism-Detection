from InputSanitizer import clean


# a custom string
class WordComparer:
    def __init__(self, synonyms_file_name):

        # a map used to store the line number for each word in the synonyms file
        # this is more efficient than storing the words themselves
        # because when we need to check if two words are synonyms
        # we only compare their line number instead of comparing two strings
        self.line_number = {}

        # construct the word mappings
        synonyms_file = None
        try:
            synonyms_file = open(synonyms_file_name, "r")
            index = 0
            for line in synonyms_file:
                # we assume that each word appear only once in the synonyms file
                for word in line.split(" "):
                    self.line_number[clean(word)] = index
                index += 1
        except FileNotFoundError:
            print("synonyms file is invalid")
            exit(-1)
        finally:
            if not synonyms_file is None:
                synonyms_file.close()

    # check if two string are synonyms using the synonyms file
    def is_same(self, s1, s2):
        # shortcut "OR" to avoid string comparison unless it's necessary
        if (s1 in self.line_number and s2 in self.line_number and self.line_number[s1] == self.line_number[s2]) or (
                    s1 == s2):
            return True
        return False
