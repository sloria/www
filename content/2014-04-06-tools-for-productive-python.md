title: Three Command-line Tools for Productive Python Development
tags: python
description: Time-saving tools for developing in Python.
category: programming

Below are three tools that I started using recently that I have since found indispensable when developing with Python.

## I. Bootstrap your project with **cookiecutter**

I am a big fan of project templates. They enable you to reuse best practices and patterns whenever you start a new project.

Audrey Roy's [cookiecutter][cookiecutter] tool makes project templates easy to use and create. Just run the `cookiecutter` command, answer some questions about your project, and cookiecutter will create an entire scaffold for your project. 

<img src="https://raw.github.com/audreyr/cookiecutter/aa309b73bdc974788ba265d843a65bb94c2e608e/cookiecutter_medium.png" width="300" alt="cookiecutter logo">

### Installing and using cookiecutter

To get the cookiecutter CLI, install with pip.

```bash
$ pip install cookiecutter
```

Choose a template and copy its git URL. There are a number of [available Python templates](https://github.com/audreyr/cookiecutter#python).

Run the `cookiecutter` command with the git URL.

```bash
$ cookiecutter https://github.com/pydanny/cookiecutter-django.git
```

Answer the prompts that appear, and you're done!


## II. Automatically activate your virtual environment with **autoenv**

Sometimes you forget to activate your project's virtual environment. Never again with Kenneth Reitz's [autoenv][].

[autoenv][] automatically executes code when you `cd` into a directory with a `.env` file. You can use it to automatically activate a project's virtual environment.

### Installing and using autoenv

If you are on a Mac with [homebrew](http://homebrew.sh), run:

```bash
$ brew install autoenv
$ echo 'source /usr/local/opt/autoenv/activate.sh' >> ~/.bash_profile
```

<aside>
Note: If you are using zsh, change "~/.bash_profile" to "~/.zshrc".
</aside>

You can also use [pip or git](https://github.com/kennethreitz/autoenv#install) to install on other platforms.

Drop a `.env` file in your project's directory with the command to activate its environment.

```bash
# .env
source activate path/to/env/bin/activate

# Or, for virtualenvwrapper:
# workon myproject 

# Or, for anaconda:
# source activate myproject
```

## III. Auto-import modules and functions into your shell sessions with **konch**

Importing the same packages, modules, and classes every time you run the Python shell is tedious. That's why I created [konch][].

Inspired by [Flask-Script][] and the [shell_plus][] command from [django-extensions](http://django-extensions.readthedocs.org/en/latest/index.html), konch allows you to create project-specific namespaces for your Python shell. You can even configure your shell's [welcome banner and input prompt](http://konch.readthedocs.org/en/latest/#konch-init).

<img src="https://dl.dropboxusercontent.com/u/1693233/blog/konch-logo.png" width="200" alt="konch logo">

### Installing and using konch

Install with `pip`.

```bash
$ pip install konch
```

In your project directory, create a new `.konchrc` file with `konch init`.

```bash
$ konch init
```

Edit the `context` dictionary in your `.konchrc` to include anything you want accessible in your shell sessions.

```python
""".konchrc."""
import konch
import mypackage
from mypackage import cheese

konch.config({
    'context': {
        'mypackage': mypackage,
        'cheese': cheese,
        'bleu': cheese.bleu,
        'cheddar': cheese.cheddar
    }
})
```

Run `konch` to start your shell.

```bash
$ konch
```

## A Note for Git Users

If you don't want your `.env` and `.konchrc` files to show up in source control, you can add them to a [global .gitignore](https://help.github.com/articles/ignoring-files#create-a-global-gitignore) file.

```bash
$ git config --global core.excludesfile ~/.gitignore_global
$ echo ".env\n.konchrc" >> ~/.gitignore_global
```

## Related Links

- [cookiecutter on Github][cookiecutter] and [docs](http://cookiecutter.readthedocs.org/en/latest/)
- [autoenv on Github][autoenv]
- [konch on Github][konch] and [docs](http://konch.readthedocs.org/en/latest/)


[cookiecutter]: https://github.com/audreyr/cookiecutter
[autoenv]: https://github.com/kennethreitz/autoenv
[konch]: https://github.com/sloria/konch
[yak shaving]: http://projects.csail.mit.edu/gsb/old-archive/gsb-archive/gsb2000-02-11.html
[Flask-Script]: https://github.com/smurfix/flask-script
[shell_plus]: http://django-extensions.readthedocs.org/en/latest/shell_plus.html

