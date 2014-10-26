title: Tutorial: Simple Text Classification with Python and TextBlob
category: programming
tags: python, textblob
slug: how-to-build-a-text-classification-system-with-python-and-textblob

*Edit October 26, 2014*: Update imports for TextBlob>=0.8.0. Thanks Justyna Chromik for pointing this out.

*Edit February 22, 2014*: Update command to download corpora. Thanks `Jason` for pointing this out.

Yesterday, [TextBlob 0.6.0][TextBlob] was released ([changelog][]), which introduces Naive Bayes classification. This tutorial shows how to use TextBlob to create your own text classification systems.

The tutorial assumes that you have <strike>TextBlob >= 0.6.0 and nltk >= 2.0</strike> TextBlob >= 8.0 installed. If you don't yet have TextBlob or need to upgrade, run:

```bash
$ pip install -U textblob nltk
```

If this is your first time installing TextBlob, you may have to download the necessary NLTK corpora. This can be done with one command:

<strike>
```bash
$ curl https://raw.github.com/sloria/TextBlob/master/download_corpora.py | python
```
</strike>

Edit: As of version 0.8.4, corpora should be downloaded with this command:

```bash
$ >python -m textblob.download_corpora
```

## Part 1: A Tweet Sentiment Analyzer (Simple classification)

Our first classifier will be a simple sentiment analyzer trained on a small dataset of fake tweets.

To begin, we'll import the `text.classifiers` and create some training and test data.

```python
from textblob.classifiers import NaiveBayesClassifier

train = [
    ('I love this sandwich.', 'pos'),
    ('This is an amazing place!', 'pos'),
    ('I feel very good about these beers.', 'pos'),
    ('This is my best work.', 'pos'),
    ("What an awesome view", 'pos'),
    ('I do not like this restaurant', 'neg'),
    ('I am tired of this stuff.', 'neg'),
    ("I can't deal with this", 'neg'),
    ('He is my sworn enemy!', 'neg'),
    ('My boss is horrible.', 'neg')
]
test = [
    ('The beer was good.', 'pos'),
    ('I do not enjoy my job', 'neg'),
    ("I ain't feeling dandy today.", 'neg'),
    ("I feel amazing!", 'pos'),
    ('Gary is a friend of mine.', 'pos'),
    ("I can't believe I'm doing this.", 'neg')
]
```

We create a new classifier by passing training data into the constructor for a `NaiveBayesClassifier`.

```python
cl = NaiveBayesClassifier(train)
```

We can now classify arbitrary text using the `NaiveBayesClassifier.classify(text)` method.

```python
cl.classify("Their burgers are amazing")  # "pos"
cl.classify("I don't like their pizza.")  # "neg"
```

Another way to classify strings of text is to use `TextBlob` objects.
You can pass classifiers into the constructor of a TextBlob.

```python
from textblob import TextBlob
blob = TextBlob("The beer was amazing. "
                "But the hangover was horrible. My boss was not happy.",
                classifier=cl)
```

You can then call the `classify()` method on the blob.

```python
blob.classify()  # "neg"
```

You can also take advantage of TextBlob's sentence tokenization and classify each sentence indvidually.

```python
for sentence in blob.sentences:
    print(sentence)
    print(sentence.classify())
# "pos", "neg", "neg"
```

Let's check the accuracy on the test set.

```python
cl.accuracy(test)
# 0.83
```

We can also find the most informative features:

```python
cl.show_informative_features(5)
# Most Informative Features
#             contains(my) = True              neg : pos    =      1.7 : 1.0
#             contains(an) = False             neg : pos    =      1.6 : 1.0
#             contains(my) = False             pos : neg    =      1.3 : 1.0
#          contains(place) = False             neg : pos    =      1.2 : 1.0
#             contains(of) = False             pos : neg    =      1.2 : 1.0
```

This indicates that tweets containing the word "my" but not containing the word "place" tend to be negative.

Here is the full script:

<script src="https://gist.github.com/sloria/6338202.js"> </script>

## Part 2: Adding More Data from NLTK

We can improve our classifier by adding more training and test data. Here we'll add data from the movie review corpus which was downloaded with NLTK.

```python
import random
from nltk.corpus import movie_reviews

reviews = [(list(movie_reviews.words(fileid)), category)
              for category in movie_reviews.categories()
              for fileid in movie_reviews.fileids(category)]
new_train, new_test = reviews[0:100], reviews[101:200]
```

Let's see what one of these documents looks like.

```python
print(new_train[0])
```

This outputs:

```python
(['kolya', 'is', 'one', 'of', 'the', 'richest', 'films', 'i', "'", 've', 'seen', 'in', 'some', 'time'
, '.', 'zdenek', 'sverak', 'plays', 'a', 'confirmed', 'old', 'bachelor', '(', 'who', "'", 's', 'likel
y', 'to', 'remain', 'so', ')', ',', 'who', 'finds', 'his', 'life', 'as', 'a', 'czech', 'cellist', 'in
creasingly', 'impacted', 'by', 'the', 'five', '-', 'year', 'old', 'boy', 'that', 'he', "'", 's', 'tak
ing', 'care', 'of', '.', 'though', 'it', 'ends', 'rather', 'abruptly', '--', 'and', 'i', "'", 'm', 'w
hining', ',', "'", 'cause', 'i', 'wanted', 'to', 'spend', 'more', 'time', 'with', 'these', 'character
s', '--', 'the', 'acting', ',', 'writing', ',', 'and', 'production', 'values', 'are', 'as', 'high', '
as', ',', 'if', 'not', 'higher', 'than', ',', 'comparable', 'american', 'dramas', '.', 'this', 'fathe
r', '-', 'and', '-', 'son', 'delight', '--', 'sverak', 'also', 'wrote', 'the', 'script', ',', 'while'
, 'his', 'son', ',', 'jan', ',', 'directed', '--', 'won', 'a', 'golden', 'globe', 'for', 'best', 'for
eign', 'language', 'film', 'and', ',', 'a', 'couple', 'days', 'after', 'i', 'saw', 'it', ',', 'walked
', 'away', 'an', 'oscar', '.', 'in', 'czech', 'and', 'russian', ',', 'with', 'english', 'subtitles',
'.'], 'pos')
```

Notice that unlike the data in Part 1, the text comes as a list of words instead of a single string. TextBlob is smart about this; it will treat both forms of data as expected.

We can now update our classifier with the new training data using the `update(new_data)` method, as well as test it using the larger test dataset.

```python
cl.update(new_train)
accuracy = cl.accuracy(test + new_test)
```

Here's the full, updated script:

<script src="https://gist.github.com/sloria/6338376.js"> </script>

## Part 3: Language Detector (Custom Feature Extraction)

An important aspect that I haven't yet mentioned is how features are being extracted from the text.

For a given `document` and training set `train`, TextBlob's default behavior is to compute which words in `train` are present in `document`. For example, the sentence "It's just a flesh wound." might have features `contains(flesh): True`, `contains(wound): True`, and `contains(knight): False`.

Of course, this simple feature extractor may not be appropriate for all problems. Here we'll create a custom feature extractor for a language detector.

Here's the training and test data.

```python
train = [
    ("amor", "spanish"),
    ("perro", "spanish"),
    ("playa", "spanish"),
    ("sal", "spanish"),
    ("oceano", "spanish"),
    ("love", "english"),
    ("dog", "english"),
    ("beach", "english"),
    ("salt", "english"),
    ("ocean", "english")
]
test = [
    ("ropa", "spanish"),
    ("comprar", "spanish"),
    ("camisa", "spanish"),
    ("agua", "spanish"),
    ("telefono", "spanish"),
    ("clothes", "english"),
    ("buy", "english"),
    ("shirt", "english"),
    ("water", "english"),
    ("telephone", "english")
]
```

A feature extractor is simply a function that takes an argument `text` (the text to extract features from) and returns a dictionary of features.

Let's create a very simple extractor that uses the last letter of a given word as its only feature.

```python
def extractor(word):
    feats = {}
    last_letter = word[-1]
    feats["last_letter({0})".format(last_letter)] = True
    return feats

print(extractor("python"))  # {'last_letter(n)': True}
```

We can pass this feature extractor as the second argument to the constructor of a `NaiveBayesClassifier`.

```python
lang_detector = NaiveBayesClassifier(train, feature_extractor=extractor)
```

And again, compute accuracy and informative features.

```python
lang_detector.accuracy(test)  # 0.7
lang_detector.show_informative_features(5)
# Most Informative Features
#           last_letter(o) = None           englis : spanis =      1.6 : 1.0
#           last_letter(l) = None           englis : spanis =      1.2 : 1.0
#           last_letter(n) = None           spanis : englis =      1.2 : 1.0
#           last_letter(h) = None           spanis : englis =      1.2 : 1.0
#           last_letter(e) = None           spanis : englis =      1.2 : 1.0
```

Not surprisingly, words that do *not* end with the letter "o" tend to be English.

Full script:

<script src="https://gist.github.com/sloria/6342158.js"> </script>

## Conclusion

TextBlob makes it easy to create your own custom text classifiers. Always remember that there is [no free lunch](http://www.no-free-lunch.org/) in machine learning, and every problem requires extensive experimentation. Happy experimenting.

## Further Reading

- [TextBlob documentation][TextBlob]
- [Naive Bayes Classification on Wikipedia](https://en.wikipedia.org/wiki/Naive_Bayes_classifier)
- [The NLTK Book, Ch. 6: Learning to Classify Text](http://nltk.googlecode.com/svn/trunk/doc/book/ch06.html)

[TextBlob]: https://textblob.readthedocs.org/en/latest/
[changelog]: https://textblob.readthedocs.org/en/latest/changelog.html#id1
