title: Tutorial: Finding Important Words in Text Using TF-IDF
category: programming
tags: python, textblob
slug: finding-important-words-in-a-document-using-tf-idf

*Edit May 25, 2015*: Fix incorrect filter in `n_containing`. Thanks Chen Liang for reporting.
*Edit October 26, 2014*: Update imports for TextBlob>=0.8.0.

 Another [TextBlob][] release (0.6.1, [changelog](https://textblob.readthedocs.io/en/latest/changelog.html)), another quick tutorial. This one's on using the [TF-IDF][] algorithm to find the most important words in a text document. It's simpler than you might think.

## What is TF-IDF?

TF-IDF stands for "Term Frequency, Inverse Document Frequency". It is a way to score the importance of words (or "terms") in a document based on how frequently they appear across multiple documents.

### Intuitively...

* If a word appears frequently in a document, it's important. Give the word a high score.
* But if a word appears in many documents, it's not a unique identifier. Give the word a low score.

Therefore, common words like "the" and "for", which appear in many documents, will be scaled down. Words that appear frequently in a *single* document will be scaled up.

## In code

The code here is tested on Python 3 with [TextBlob 0.6.1][TextBlob].
If you're using Python 2, you'll probably need to add `# -*- coding: utf-8 -*-` and
`from __future__ import division, unicode_literals` at the top.

```python
import math
from textblob import TextBlob as tb

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)
```

14 lines and we're already [flying](http://xkcd.com/353/).

* `tf(word, blob)` computes "term frequency" which is the number of times a word appears in a document `blob`, normalized by dividing by the total number of words in `blob`. We use TextBlob for breaking up the text into words and getting the word counts.
* `n_containing(word, bloblist)` returns the number of documents containing `word`. A [generator expression](http://www.python.org/dev/peps/pep-0289/) is passed to the `sum()` function.
* `idf(word, bloblist)` computes "inverse document frequency" which measures how common a word is among all documents in `bloblist`. The more common a word is, the lower its `idf`. We take the ratio of the total number of documents to the number of documents containing `word`, then take the `log` of that. Add 1 to the divisor to prevent division by zero.
* `tfidf(word, blob, bloblist)` computes the TF-IDF score. It is simply the product of `tf` and `idf`.

Now to test it out on some real documents taken from Wikipedia.

```python
document1 = tb("""Python is a 2000 made-for-TV horror movie directed by Richard
Clabaugh. The film features several cult favorite actors, including William
Zabka of The Karate Kid fame, Wil Wheaton, Casper Van Dien, Jenny McCarthy,
Keith Coogan, Robert Englund (best known for his role as Freddy Krueger in the
A Nightmare on Elm Street series of films), Dana Barron, David Bowe, and Sean
Whalen. The film concerns a genetically engineered snake, a python, that
escapes and unleashes itself on a small town. It includes the classic final
girl scenario evident in films like Friday the 13th. It was filmed in Los Angeles,
 California and Malibu, California. Python was followed by two sequels: Python
 II (2002) and Boa vs. Python (2004), both also made-for-TV films.""")

document2 = tb("""Python, from the Greek word (πύθων/πύθωνας), is a genus of
nonvenomous pythons[2] found in Africa and Asia. Currently, 7 species are
recognised.[2] A member of this genus, P. reticulatus, is among the longest
snakes known.""")

document3 = tb("""The Colt Python is a .357 Magnum caliber revolver formerly
manufactured by Colt's Manufacturing Company of Hartford, Connecticut.
It is sometimes referred to as a "Combat Magnum".[1] It was first introduced
in 1955, the same year as Smith &amp; Wesson's M29 .44 Magnum. The now discontinued
Colt Python targeted the premium revolver market segment. Some firearm
collectors and writers such as Jeff Cooper, Ian V. Hogg, Chuck Hawks, Leroy
Thompson, Renee Smeets and Martin Dougherty have described the Python as the
finest production revolver ever made.""")

bloblist = [document1, document2, document3]
for i, blob in enumerate(bloblist):
    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:3]:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
```

For each document, we store the TF-IDF scores in a dictionary `scores` mapping `word => score` using a [dict comprehension](http://www.python.org/dev/peps/pep-0274/). We then sort the words by their scores and output the top 3 words.

The full script is [here](https://gist.github.com/6407257). The output of the program is:

```
Top words in document 1
    Word: films, TF-IDF: 0.00997
    Word: film, TF-IDF: 0.00665
    Word: California, TF-IDF: 0.00665
Top words in document 2
    Word: genus, TF-IDF: 0.02192
    Word: among, TF-IDF: 0.01096
    Word: Currently, TF-IDF: 0.01096
Top words in document 3
    Word: Magnum, TF-IDF: 0.01382
    Word: revolver, TF-IDF: 0.01382
    Word: Colt, TF-IDF: 0.01382
```

There may be ways to improve the our TF-IDF algorithm, such as by ignoring stopwords or using a different `tf` scheme. I'll leave it up to the reader to experiment.

### Further reading

* [TF-IDF on Wikipedia][TF-IDF]
* [Machine Learning with Python: Meeting TF-IDF for Text Mining](http://aimotion.blogspot.com/2011/12/machine-learning-with-python-meeting-tf.html)
* [Short introduction to Vector Space Model](http://pyevolve.sourceforge.net/wordpress/?p=1589)

[TextBlob]: https://textblob.readthedocs.io/en/latest/
[TF-IDF]: https://en.wikipedia.org/wiki/Tf%E2%80%93idf
