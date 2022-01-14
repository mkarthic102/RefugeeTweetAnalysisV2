from wordsegment import load, segment
import preprocessor as pre
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv


def process_tweet(line):
    """
    Remove hashes, numbers, and unnecessary words (such as 'rt', which stands for 'retweet')
    Segments the tweet (including hashtags) into individual words

    :param line: the tweet to be processed
    :return: processed tweet
    """
    line1 = re.sub(r'rt', '', line)
    line2 = re.sub(r'[0-9]+', '', line1)
    line3 = re.sub(r'#', '', line2)
    line4 = segment(str(line3))  # Creates an array of words
    line5 = ' '.join(map(str, line4))  # Converts array into a String
    return line5


def create_array_of_tweets(file_name):
    """
    Creates an array of processed tweets (no mentions or numbers & hashtags split into individual words)

    :param file_name: the file of tweets
    :return: an array of processed tweets
    """

    # Sets options for tweet processing (removes url, mentions, and emojis)
    pre.set_options(pre.OPT.URL, pre.OPT.EMOJI, pre.OPT.MENTION, pre.OPT.SMILEY)

    # Loads wordsegment package
    load()

    # Creates an array of tweets
    # No mentions or numbers. Hashtags are split into individual words
    with open(file_name, "r") as train_tweets:
        processed_tweets = []
        for line in train_tweets:
            line = process_tweet(pre.clean(line))
            processed_tweets.append(line)

    return processed_tweets


def sentiment_score(array):
    """
    Uses VADER to determine the sentiment score of each tweet

    :param array: array of tweets
    :return: none
    """

    # Creates a SentimentIntensityAnalyzer object.
    sent_obj = SentimentIntensityAnalyzer()

    # Variables to keep track of the number of tweets and total polarity
    total_tweets = 0
    total_polarity = 0

    # Variables to keep track of total number of positive, negative, and neutral tweets
    total_positive = 0
    total_neutral = 0
    total_negative = 0

    for line in array:
        # Sentiment dictionary that contains scores
        sentiment_dict = sent_obj.polarity_scores(line)

        """
        print(line)
        print("Overall sentiment dictionary is : ", sentiment_dict)
        print("Sentence was rated as ", sentiment_dict['neg'] * 100, "% Negative")
        print("Sentence was rated as ", sentiment_dict['neu'] * 100, "% Neutral")
        print("Sentence was rated as ", sentiment_dict['pos'] * 100, "% Positive")
        """

        # Keeps track of the total number of tweets and total polarity
        # To find average polarity later
        total_tweets += 1
        total_polarity += sentiment_dict['compound']

        # Determines the overall sentiment of the tweet
        if sentiment_dict['compound'] >= 0.05:
            # sentiment = "Positive"
            total_positive += 1

        elif sentiment_dict['compound'] <= - 0.05:
            # sentiment = "Negative"
            total_negative += 1

        else:
            # sentiment = "Neutral"
            total_neutral += 1

        """
        print("Sentence Overall Rated As " + sentiment)
        print()
        """

    # Average overall sentiment
    average_sentiment = total_polarity / total_tweets

    if average_sentiment >= 0.05:
        overall_sentiment = "Positive"

    elif average_sentiment <= - 0.05:
        overall_sentiment = "Negative"

    else:
        overall_sentiment = "Neutral"

    print("Overall Sentiment of Tweets: ", overall_sentiment)

    # Percent of tweets with positive, negative, or neutral sentiments
    percent_positive = (total_positive / total_tweets) * 100
    percent_negative = (total_negative / total_tweets) * 100
    percent_neutral = (total_neutral / total_tweets) * 100

    print("Percent of Positive Tweets: %", str(round(percent_positive, 2)))
    print("Percent of Negative Tweets: %", str(round(percent_negative, 2)))
    print("Percent of Neutral Tweets: %", str(round(percent_neutral, 2)))

    create_file(percent_positive, percent_negative, percent_neutral)


def create_file(percent_positive, percent_negative, percent_neutral):
    """
    Creates a csv file in order to visualize the data in R

    :param percent_positive: percent of positive tweets
    :param percent_negative: percent of negative tweets
    :param percent_neutral: percent of neutral tweets
    :return:
    """

    fields = ['Percent Positive', 'Percent Negative', 'Percent Neutral']
    rows = [[percent_positive, percent_negative, percent_neutral]]
    filename = "sentiment_percentages.csv"

    with open(filename, 'w') as csvfile:
        # Creates a csv writer object
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)


def main():
    processed_tweets = create_array_of_tweets("test-cleaned.txt")
    sentiment_score(processed_tweets)


if __name__ == "__main__":
    main()
