import csv
import collections
from googleapiclient.discovery import build
from time import sleep
import pandas as pd
import re
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os


def scrape_comments(video_id, api_key, max_comments)-> list[str]:
    """
    Generates a list of strings from the comments on a YouTube video, does not save to a file
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




# Extracts the words from comments on a Youtube Video and saves to a data file
def load_comments(video_id: str, api_key: str, x) -> str:  # Returns filename
    API_KEY = api_key
    youtube = build("youtube", "v3", developerKey=API_KEY)
    output_file = f'{video_id}_youtube_comments.csv'
    number_of_comments = x # Extracts number of comments passed as argument
    comment_counter = 0 # Track total number of comments collected

    # Saves output file in separate results folder
    base_directory = os.path.join("..", "data")
    output_folder = os.path.join(base_directory, "youtube_comments")
    os.makedirs(output_folder, exist_ok=True)
    output_file_path = os.path.join(output_folder, output_file)

    print(f"Retrieving max of {number_of_comments} comments for: {video_id}")

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
            df.to_csv(output_file_path, index=False, encoding = "utf-8")
            sleep(2)
            request = youtube.commentThreads().list_next(request, response)
            print("Iterating through next page...")

            total_comments = len(comments)
            print(f"{total_comments} comments extracted to filepath: {output_file_path}")

        except Exception as e:
            print(f"Error while loading comments: {e}")

    if output_file_path:
        return output_file_path
    else:
        return ""



# Word Cloud Generator
def get_top_word_cloud(video_id: str, number_of_words: int):
    """
    Generates a word cloud of top most used words in comments pertaining to key_word (title, actor, platform etc)
    Returns the filename word cloud image
    """
    key_location = input("key file path: ")
    api_key = connect_api_key(key_location)
    comments = scrape_comments(video_id, api_key, 1000)
    text = " ".join(comments)


    # Ignores common irrelevant words
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
        base_directory = os.path.join("..", "data")     # Saves the results under the data folder
        output_folder = os.path.join(base_directory, "youtube_comments")
        os.makedirs(output_folder, exist_ok=True)
        filename = str(f"{video_id}_wordcloud.png")
        filepath = os.path.join(output_folder, filename)
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

    return

# testing
# video_id = "0SKOObeuGuA"
# key_file = "../../keys/youtube_key.txt"
# key = connect_api_key(key_file)
# scrape_comments(video_id, key, 200)
