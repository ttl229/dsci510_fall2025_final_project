from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


def create_word_cloud(text) -> WordCloud:

    stopwords = set(STOPWORDS)
    stopwords.update("the", "is", "a")

    wordcloud = WordCloud(
        background_color="white",
        max_words = 50,
        stopwords = stopwords,
        width = 600,
        height = 400
    ).generate(text)

    print("Displaying word cloud...")

    # Display generated word cloud as image
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show(block=False)
    plt.pause(2)
    plt.close()

    wordcloud_image = wordcloud

    return wordcloud_image
