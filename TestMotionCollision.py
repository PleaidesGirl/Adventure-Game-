import re, operator

# Initial code written by David Johnson, University of Utah.
# Author of final code: Celine Cavanaugh, Ivan Lee


#
#
# This section of code is fully implemented and provided for you to use.
#
#

# This function is called with a dictionary. It will return
# a list of tuples in the form (key, value) and ordered by
# the value in value. So given a
# dict = {"c":12, "a":2, "b":1}
# it will return a list
# [("b",1), ("a",2), ("c",12)]
def make_sorted_list_by_value_from_dictionary(dict):
    return sorted(dict.items(), key=operator.itemgetter(1))

# This function removes everything except the letters a-z from words.
# So it removes punctuation, unusual accented letters, etc.
def remove_punctuation(words):
    clean_words = []
    for word in words:
        clean_word = re.sub("[^a-z ]+", "", word)
        if len(clean_word) > 0:
            clean_words.append(clean_word)
    return clean_words

# This function reads the 'stop_words.txt' file and returns each word from the file in a list.
def read_common_words():
    stopWords = []
    with open('stop_words.txt','r') as file:
        for word in file:
            word = word.strip() # There are some hidden characters in the file that need to be removed
            stopWords.append(word)
    return stopWords

# Given a list of words, break the list into chunks of length chunk_size (the last chunk
# is just whatever is left over). Create a list of these chunks and return that.
# Given a list
# ['a', 'boy', 'is', 'a', 'very', 'good', 'boy']
# and a chunk_size of 2, this would return a list of chunks of length 2
# [['a', 'boy'], ['is', 'a'], ['very', 'good'], ['boy']]
# This function is implemented for you.
def break_words_into_chunks(text_words, chunk_size):
    chunk_list = []
    for index in range(0, len(text_words), chunk_size):
        chunk_list.append(text_words[index:index+chunk_size])
    return chunk_list

#
#
# This section of code needs to be implemented by you.
#
#


# Given a filename, open that file, read all the lines and return a list of all the words in the file.
# Use split() to break a line into words.
def read_all_words_in_file(filename):

    words = list()

    with open (filename) as file:
        for line in file:
            sentenceWords = line.split()
            for word in sentenceWords:
                words.append(word)
    return words



# Given a list of words, return a new list with all the words lower case. Use
# the string lower() method to make the word lower case.
def make_lowercase(words):
    newlist = list()
    for word in words:
        newWord = str(word).lower()
        newlist.append((newWord))
    return newlist

# This function makes a new list from book_words that has all the words in
# common_words removed. Go through the words in book_words and add it to the
# new list if the word isn't in the common_words list. Return the new list.
def remove_common_words(book_words, common_words):
    newlist = list()
    for word in book_words:
        if not common_words.__contains__(word):
            newlist.append(word)
    return newlist

# Given a list of text_words and another list of words, count how many times
# any word in text_words has a match in other_list.
# For
# text_words = ['a', 'the', 'a', 'boy']
# and
# other_list = ['a', 'the']
# this function would return 3, since 'a' appears 2 times, 'the' once, and 'boy'
# no times.
# Recall that the "in" operator is a good way of telling if a value is in a list.
def count_number_of_words_that_appear_in_another_list(text_words, other_list):
    word_count = 0
    for word in text_words:
        if other_list.__contains__(word):
            word_count += 1
    return word_count

# Calculate the average length of all the words in text_words.
# Add up the length of each word and divide by the number of words.
# Return that average.
def average_word_length(text_words):
    total_words = 0
    total_word_length = 0
    for word in text_words:
        total_words += 1
        total_word_length = total_word_length + len(word)
        average_length = total_word_length/total_words
        #I'm not sure if this works
    return average_length # Need to implement this function

# Make a dictionary that has words of text_words as keys and how many
# times that word appears in text_words as the value.
# Refer to the lecture slides for how to do this.
# Return the dictionary.
def calculate_word_frequency(text_words):
    word_frequency = {}
    for word in text_words:
        if word in word_frequency:
            word_frequency[word] += 1
        else:
            word_frequency[word] = 1
    return word_frequency

# Count the words in word_list that appear in positive_words, then count the
# words in word_list that appear in negative words.
# Turn each count into a percentage by dividing by the length of word_list and then
# multiply by 100.
# Return the difference between the positive percentage and the negative percentage rounded
# to 2 decimal places. The code for rounding is provided.
# A positive returned number means there were more positive than negative words.
# As an example, if
# word_list = ['a', 'sad', 'boy', 'is', 'an', 'excellent', 'good', 'boy']
# positive_words = ['excellent', 'good']
# negative_words = ['sad']
# The positive count would be 2 (for excellent and good)
# The negative count would be 1 (for sad)
# The positive percentage would be 2/8 * 100 = 25
# the negative percentage would be 1/8 * 100 = 12.5
# The returned value would be 25 - 12.5 = 12.50.
# You should use the count_number_of_words_that_appear_in_another_list function to do the counting.
def calculate_sentiment(word_list, positive_words, negative_words):
    total_word = 0
    positive_amount = 0
    negative_amount = 0
    for word in word_list:
        total_word += 1
        if positive_words.__contains__(word):
            positive_amount += 1
        if negative_words.__contains__(word):
            negative_amount += 1
    positive_percentage = positive_amount / total_word * 100
    negative_percentage = negative_amount / total_word * 100
    difference = positive_percentage - negative_percentage
    return round(difference,2) # Implement and replace 0.0 with the difference between the positive and negative percents.


# This code runs when the file is executed and is fully implemented.
def main():

    # Read in the positive and negative words for later use.
    positive_words = read_all_words_in_file("positive.txt")
    negative_words = read_all_words_in_file("negative.txt")

    # Analyze the following files. You may want to comment out all files but 1 when testing.
    files = ["HuckFinn.txt", "TheScarletLetter.txt", "Plato.txt", "TaleOfTwoCities.txt"]

    # Loop over all the files
    for file in files:
        # Report on which file is being analyzed
        print("\n\nAnalyzing:", file)

        # get the words from the text and clean them up
        print("Getting words from book")
        book_words = read_all_words_in_file(file)
        book_words = make_lowercase(book_words)
        #book_words = remove_punctuation(book_words)
        print("    ", len(book_words), " words found")

        # Remove common words
        common_words = read_common_words()
        print("Removing common words")
        book_words = remove_common_words(book_words, common_words)
        print("    ", len(book_words), " words remaining")

        # Break the list of words into 20 chunks
        chunks = break_words_into_chunks(book_words, len(book_words)//20 + 1)

        # Look at overall and chunk sentiment
        print("Calculating Sentiment")
        print("    Overall:", calculate_sentiment(book_words, positive_words, negative_words))
        print("    Chunk Sentiment: ", end='')
        for chunk in chunks:
            print(calculate_sentiment(chunk, positive_words, negative_words), end=' ')
        print()

        # Find the average word length
        print("Average word length:", round(average_word_length(book_words),1))

        # Count up the most common words and report on the top 10.
        print("Counting most common words")
        word_frequencies = calculate_word_frequency(book_words)
        word_frequency_list = make_sorted_list_by_value_from_dictionary(word_frequencies)
        word_frequency_list.reverse()
        print("    Most common words:", word_frequency_list[:10])


# This runs if the file is executed and doesn't if the file is imported
if __name__ == '__main__':
    main()
