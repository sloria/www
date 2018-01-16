title: Python Best Practice Patterns by Vladimir Keleshev (Notes)
category: programming
tags: python, notes
slug: python-best-practice
alias: /python-best-practice-patterns-by-vladimir-keleshev-notes/
date: 2013-05-09

These are my notes from Vladimir Keleshev's talk entitled "Python Best Practice Patterns", given on May 2, 2013 at the Python Meetup in Denmark. The original video is [here](http://youtu.be/GZNUfkVIHAY) (about 38 minutes long).

Note: Some of the code examples have been has been modified from the original presentation based on readers' feedback.

## Composed method

- Divide program into methods that perform one task
    - Keep *all* operation in a method at the same level of abstraction
- Use many methods only a few lines long


- Different levels of abstraction: bitmaps, filesystem operations, playing sounds...

<script src="https://gist.github.com/sloria/5895673.js"> </script>

- `safety_check` deals with temp and pressure
- `alarm` deals with files and sound
- `pressure` deals with bits and converting them

## Constructor method

- provide constructors that create well-formed instances
    - Pass all required parameters to them

[gist:id=5895677]

- Can use class methods to make multiple constructors
    - Example: Using Cartesian or polar coordinates

[gist:id=5895679]


## Method objects
- How do you code a method where many lines of code share many arguments and temporary variables?

<script src="https://gist.github.com/sloria/5895682.js"> </script>

- Can't be solved by making many small methods (would use more code)

<script src="https://gist.github.com/sloria/5895686.js"> </script>

## Execute around method (in Python: Context manager)
- How do you represent pairs of actions that should be taken together?

<script src="https://gist.github.com/sloria/5895687.js"> </script>

## Debug printing method
- `__str__` for users
    - e.g. `print(point)`
- `__repr__` for debugging/interactive mode

## Method comment
- small methods can be more effective than comments

<script src="https://gist.github.com/sloria/5895694.js"> </script>

## Choosing message

<script src="https://gist.github.com/sloria/5895717.js"> </script>

## Intention revealing message
- How do you communicate your intent when implementation is simple?
- Use for methods that do the same thing (for readability)

<script src="https://gist.github.com/sloria/5895726.js"> </script>

## Constant method (constant class variable)

<script src="https://gist.github.com/sloria/5895732.js"> </script>

- Depends if you are designing to make your class subclassable

## Direct and indirect variable access
- Direct
    - no need for getters and setters

<script src="https://gist.github.com/sloria/5895737.js"> </script>

## Enumeration (iteration) method

<script src="https://gist.github.com/sloria/5895749.js"> </script>

## Temporary variable

<script src="https://gist.github.com/sloria/5895751.js"> </script>

## Sets
- Can often use sets instead of combination of `for` loops

<script src="https://gist.github.com/sloria/5895758.js"> </script>

## Equality method
<script src="https://gist.github.com/sloria/5895762.js"> </script>

- Probably the only case to check `isinstance()`

## Hashing method
<script src="https://gist.github.com/sloria/5895766.js"> </script>

## Sorted collection
<script src="https://gist.github.com/sloria/5895768.js"> </script>

## Concatenation
<script src="https://gist.github.com/sloria/5895770.js"> </script>

## Simple enumeration parameter
- When you can't come up with an iteration param that makes sense, just use `each`

<script src="https://gist.github.com/sloria/5895773.js"> </script>

## Cascades
- Instead of writing methods without return values, make them return self
    - allows cascading of methods

<script src="https://gist.github.com/sloria/5895776.js"> </script>

## Interesting return value

<script src="https://gist.github.com/sloria/5895782.js"> </script>

- Explicit better than implicit
- Include return value if it's interesting (even if it's `None`)

## Further reading
- [Smalltalk Best Practice Patterns](http://www.amazon.com/Smalltalk-Best-Practice-Patterns-ebook/dp/B00BBDLIME/ref=dp_kinw_strp_1)
    - Not just for Smalltalk: applicable to Python, Ruby, and many other languages

## Edits

*March 14, 2014*: Fix conditional in Composed Method section. Thanks Rufus Smith.

*February 28, 2014*: `__eq__` returns `NotImplemented` to avoid asymmetric comparison. Thanks Daniel Smith.

*February 28, 2014*: Removed `enumerate` usage in  "Interesting Return Value" section. Thanks Hugh Brown and Paul Winkler.

*September 5, 2013*: Fixed error in Sorted Collection. Thanks Frank Sievertsen.

*September 4, 2013*: Fixed typo in Choosing Message gist. `instanceof()` should be `isinstance()`. Thanks to `richardborcsik` for catching this.

*July 30, 2013*: Fixed typo in Sorted Collection gist. `__lt__(self, other)` needs two arguments. Thanks to Tiago Oliveira for catching this.







