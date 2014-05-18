title: Hosting static Flask sites for free on Github Pages
category: programming
tags: python, flask

This past weekend, I released [KillTheYak.com](http://killtheyak.com/), a website with guides for installing and using various tools. It's a static site powered by [Flask][] and hosted for free on [Github Pages][].

Static Flask sites are a big win because:

- They're fast.
- If you need your site to be dynamic in the future, the transition will be easy.
- There are well-developed extensions for doing this. Here I'll demonstrate [Frozen-Flask][] (for building static content) and [Flask-FlatPages][] (for writing pages in Markdown).

Source for the example site here: [sloria/flask-ghpages-example][example]. Live site here: [http://stevenloria.com/flask-ghpages-example][live-example]

## App structure

[![App structure](https://dl.dropboxusercontent.com/u/1693233/blog/flask-ghpages-tree.png "App structure")](https://dl.dropboxusercontent.com/u/1693233/blog/flask-ghpages-tree.png)

### project/settings.py

<script src="https://gist.github.com/sloria/6004145.js"> </script>

Key bits:

- L19: Tell Frozen-Flask to build the static content to the project root instead of the default `build/` directory. 
- L22: We also need to explicitly set `FREEZER_BASE_URL` since Github Pages hosts your repo pages on `http://username.github.com/your-reponame`. 
- L23: Don't delete all your app files!
- L26-27: Tell FlatPages to look for `.md` files in the `project/pages/` directory.

### project/app.py

<script src="https://gist.github.com/sloria/6004129.js"> </script>

- This is where the Flask `app`, `pages`, and `freezer` instances live.

### project/views.py

<script src="https://gist.github.com/sloria/6004206.js"> </script>

- The `page(path)` view retrieves a page object and passes it to the template.

### project/pages/bacon.md (Page example)

<script src="https://gist.github.com/sloria/6004253.js"> </script>

- The first lines are YAML metadata. They can be accessed in views via the `page.meta` dict. For example, `page.meta['title']`. They're also accessible in the templates, as we'll see next.
- L2: Dates are parsed by PyYAML as datetime objects.

### project/templates/page.html

<script src="https://gist.github.com/sloria/6004272.js"> </script>

### project/main.py

This just imports `app`, `pages`, and `freezer`, and `views` so that they can be accessed without circular imports ([source](https://github.com/sloria/flask-ghpages-example/blob/master/project/main.py)).

### freeze.py

<script src="https://gist.github.com/sloria/6004277.js"> </script>

- This builds the static content to the project root.

## Deployment

After creating your Github repo, run the following:

<script src="https://gist.github.com/sloria/6004389.js"> </script>

That's it!

See also:

- [Example project source][example] and the [Live site][live-example]
- Another example: [Kill The Yak source][] and the [Live site][Kill The Yak]
- [Frozen-Flask home][Frozen-Flask]
- [Flask-FlatPages home][Flask-FlatPages]

[example]: https://github.com/sloria/flask-ghpages-example
[live-example]: http://stevenloria.com/flask-ghpages-example
[Flask]: http://flask.pocoo.org/
[Github Pages]: http://pages.github.com
[Kill The Yak]: http://killtheyak.com
[Kill The Yak source]: https://github.com/killtheyak/killtheyak.github.com/tree/master/killtheyak
[Frozen-Flask]: http://pythonhosted.org/Frozen-Flask/
[Flask-FlatPages]: http://pythonhosted.org/Flask-FlatPages/
