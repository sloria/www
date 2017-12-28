title: The .ideas file
tags: terminal, tips

> The best way to a good idea is to have lots of ideas. <cite>Linus Pauling</cite>

If you're a regular Terminal user, chances are you've had a stroke of inspiration while your command prompt was up.

I find plain text in [Markdown](http://daringfireball.net/projects/markdown/) to be the quickest way to record these spontaneous ideas. Here's one way to do it:

Create a hidden file called `.ideas.md` in your home directory.

```bash
$ touch ~/.ideas.md
```

Add an alias to your `.bash_profile` or `.zshrc` file so you can open the file quickly

```bash
alias idea="subl ~/.ideas.md"  # for Sublime Text users
```

**OR**

```bash
alias idea="vim ~/.ideas.md"  # for Vim users
```



Now when you have an idea, just type

```bash
$ idea
```

at the command line to open up the `.ideas.md` file in your text editor.

What you put in this file is up to you. Mine looks something like this:

```
~/.ideas.md

# Software
    - doomed startup idea 1
    - some feature for an open-source project
    - doomed startup idea 2
    - ...

# Blog posts
    - the .ideas file
    - stuff about nothing...
    - ...
```

You can do this for todo lists, schedules, or any other text document that you open regularly.
