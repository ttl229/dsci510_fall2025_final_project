from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

text = """
"""

stopwords = set(STOPWORDS)
stopwords.update("the", "is", "a")

wordcloud = WordCloud(
    background_color="white",
    max_words = 50,
    stopwords = stopwords,
    width = 600,
    height = 400
).generate(text)

plt.figure(figsize=(10, 10))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()