title: Lazily-evaluated property pattern in Python
category: programming
tags: python
slug: lazy-evaluated-properties-in-python

[Lazy evaluation](https://en.wikipedia.org/wiki/Lazy_evaluation) is a useful pattern that can improve your code's efficiency in many situations. One example of this is instance attributes that take long to compute:

<script src="https://gist.github.com/sloria/5895397.js"> </script>

This approach may cause initialization to take unnecessarily long, especially when you don't always need to access `Person#relatives`.

A better strategy would be to get `relatives` only when it's needed (i.e. "lazily"):

<script src="https://gist.github.com/sloria/5895446.js"> </script>

In this case, the list of relatives is only computed the first time `Person#relatives` is accessed. After that, it is stored in `Person#_relatives` to prevent repeated evaluations.

A perhaps more Pythonic approach would be to use a decorator that makes a property lazy-evaluated

<script src="https://gist.github.com/sloria/5895501.js"> </script>

This removes a lot of boilerplate, especially when an object has many lazily-evaluated properties.
