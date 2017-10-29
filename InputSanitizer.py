# a function to clean up words form unneeded characters
# assume all characters are lower case and only take into account alphabetical characters


def clean(s):

    s=s.lower()
    ret=""
    for c in s:
        if (c>='a' and c<='z') or c==' ':
            ret+=c
    return ret