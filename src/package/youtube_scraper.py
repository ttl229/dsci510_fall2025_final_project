import csv
import collections
from googleapiclient.discovery import build
from time import sleep
import pandas as pd
import re
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
# from database import connect_api_key

def scrape_comments(video_id, api_key, max_comments)-> list[str]:
    """
    Generates a list of of strings from the comments on a YouTube video, does not save to a file
    """
    API_KEY = api_key
    youtube = build("youtube", "v3", developerKey=API_KEY)
    comment_counter = 0  # Track total number of comments collected
    comments = [] # Initiates empty list to store comments in

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=max_comments,
    )

    while request and comment_counter < max_comments:
        try:
            response = request.execute()

            for item in response.get("items", []):
                text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(text) # Appends the comment
                comment_counter += 1 # Increments the comment counter

            if "nextPageToken" in response and comment_counter < max_comments:
                request = youtube.commentThreads().list_next(request, response)
                continue

            if comment_counter >= max_comments:
                # Stops collecting data once maximum number of comments reached
                break

        except Exception as e:
            print(f"Error while loading comments: {e}")

    return comments





def load_comments(video_id: str, api_key: str, x) -> str:  # Returns filename
    API_KEY = api_key
    youtube = build("youtube", "v3", developerKey=API_KEY)
    output_filepath = f'{video_id}_youtube_comments.csv'
    number_of_comments = x # Extracts number of comments passed as argument
    comment_counter = 0 # Track total number of comments collected

    print(f"Retrieving max of {number_of_comments} comments for: {video_id}") # Verify video ID is

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=number_of_comments,
    )

    df = pd.DataFrame(columns = ['comment_content', 'comment_date', 'user_name'])
    # Extracts by comment content, date posted, and user origin

    while request:
        # Stops collecting data once maximum number of comments reached
        if comment_counter >= number_of_comments:
            print(f"{number_of_comments} comments reached, stopping data extraction.")
            break

        try:
            response = request.execute()
            comments = []
            dates = []
            user_names = []

            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)  # Extracts top level comments as list
                date = item['snippet']['topLevelComment']['snippet']['publishedAt']
                dates.append(date) # Extracts date published for each comment
                user_name = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                user_names.append(user_name) # Extracts user name for each comment

            df2 = pd.DataFrame({"comment_content": comments, "comment_date": dates, "user_name": user_names})
            df = pd.concat([df, df2], ignore_index=True)
            df.to_csv(output_filepath, index=False, encoding = "utf-8")
            sleep(2)
            request = youtube.commentThreads().list_next(request, response)
            print("Iterating through next page...")

            total_comments = len(comments)
            print(f"{total_comments} comments extracted to filepath: {output_filepath}")

        except Exception as e:
            print(f"Error while loading comments: {e}")

    if output_filepath:
        return output_filepath
    else:
        return None


# Function to count the top words used in comments per video
def count_words(video_id:str, number_of_words: int):
    """
    Returns a dictionary of the top number of words found in comments of a video
    Example usage: Returns dictionary of top 10 most used words in comment section of a video
    """
    all_words = collections.Counter()
    # List of basic words to ignore in counter
    stop_words = ["the", "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "in", "out", "on", "off", "then", "once", "here", "there", "when", "how", "all", "any", "each", "few", "more", "most", "some", "such", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

    try:
        with open(f"{video_id}_youtube_comments.csv", "r", encoding="utf-8") as f:
            print(f"Reading all words in comments from video with videoID: {video_id}...")
            reader = csv.reader(f)
            next(reader)  # Skips the header row

            for row in reader:
                comment_text = row[0]       # Extracts the contents from the 'comment_content' column
                # Remove punctuation, special characters from words
                cleaned_text = re.sub(r'[^\w\s]','', comment_text)
                comment_words = cleaned_text.lower().split()

                for word in comment_words:
                    if word in stop_words: # Ignore common connector words
                        continue
                    if word: # Check for empty strings after cleaning
                        all_words[word] += 1

    except FileNotFoundError as e:
        print(f"Could not find comment data file for {video_id}: {e}")
        return collections.Counter() # Return empty counter

    # Sorts the dictionary by top words
    print(f"Sorting results by {number_of_words} most common words...")
    top_words = all_words.most_common(number_of_words)
    print(top_words)

    return top_words

# Word Cloud Generator
def get_top_word_cloud(key_word, number_of_words)->str:
    """
    Generates a word cloud of top most used words in comments pertaining to key_word (title, actor, platform etc)
    Returns the filename word cloud image
    """
    text = key_word

    stopwords = set(STOPWORDS)
    stopwords.update("the", "is", "a")

    try:
        wordcloud = WordCloud(
            background_color="white",
            max_words=number_of_words,
            stopwords=stopwords,
            width=600,
            height=400
        ).generate(text)

        # Save the wordcloud as a file
        filepath = str(f"{key_word[:5]}_wordcloud.png")
        wordcloud.to_file(filepath)
        print("Displaying word cloud...")

        # Display generated word cloud as image
        plt.figure(figsize=(10, 10))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show(block=False)
        plt.pause(2)
        input("Press Enter to close...")
        plt.close()

        print(f"Saved word cloud image to filepath: {filepath}")

    except Exception as e:
        print(f"Error generating word cloud. {e}")

    return filepath

# testing
# video_id = "0SKOObeuGuA"
# key_file = "../../keys/youtube_key.txt"
# key = connect_api_key(key_file)
# scrape_comments(video_id, key, 200)
