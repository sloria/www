title: Introducing local-repl: Supercharged Node.js REPLs
tags: nodejs, javascript
description: An introduction to local-repl, a CLI for running project-specific Node.js REPLs.
slug: local-repl
category: programming
status: published

Today I released [local-repl 4](https://github.com/sloria/local-repl), a CLI for running project-specific Node.js REPLs.

## The basic idea

local-repl saves you from typing out imports every time you open a new Node.js REPL.
You specify the modules and objects that you want to automatically import in
either `package.json` or `.replrc.js`.

local-repl also enables the use of `await` in the REPL, making it much
more usable when working with functions that return promises.

## Features

- Automatically import modules and values into your REPL sessions
- Use `await` in the REPL without having to wrap your code in async functions
- Configure the REPL banner and prompt

## Hello world!

Let's say that you have a project using lodash, and you want `lodash` 
available whenever you open a new REPL session. 

Install local-repl…

```
npm install local-repl --save-dev
```

…and add the following to your `package.json`.

```json
{
  "scripts": {
    "repl": "local-repl"
  },
  "repl": [
    "lodash"
  ]
}
```

Then run your REPL with

```bash
npm run repl
```

`lodash` will already be imported and ready to use.

<figure>
  <img alt="local-repl with lodash" src="https://raw.githubusercontent.com/sloria/local-repl/master/media/basic.gif" >
  <figcaption>
    So much less typing!
  </figcaption>
</figure>

## Aliasing imports

You can specify aliases for imports.

```json
{
  "repl": [
    {"name": "l", "module": "lodash"}
  ]
}
```

## More magic

Defining your REPL configuration in `package.json` is convenient, but often you'll want more flexibility. For example, you might want to query for a record in your database and include it in your REPL sessions.

You can define your configuration in a `.replrc.js` file in the root of your project.

```javascript
// .replrc.js
const User = require('./myapp/models/User');

module.exports = {
  context: {
    l: require('lodash'),
    utils: require('myapp/utils'),
    // NOTE: Promises are automagically resolved!
    me: User.getByUsername('sloria'),
  }
} 
```

Let's assume `User.getByUsername` returns a `Promise` to a User object. local-repl does the right thing and gives you the *resolved value* in your REPL session. 

## `await` support

Normally, using the `await` keyword in the REPL is clumsy, requiring you
to wrap your calls in one-off `async` functions.

local-repl allows you to use `await` without having to create any
wrapper functions.

Just add the following to your package.json:

```json
{
  "repl": {
    "enableAwait": true
  }
}
```

Or in `.replrc.js`:

```javascript
// .replrc.js
module.exports = {
  enableAwait: true
}
```

<figure>
  <img alt="await support in local-repl" src="https://raw.githubusercontent.com/sloria/local-repl/master/media/await.gif" >
  <figcaption>
    Using <code>await</code> in a REPL
  </figcaption>
</figure>


## External links

- [local-repl on GitHub](https://github.com/sloria/local-repl)
- [local-repl on NPM](https://www.npmjs.com/package/local-repl)
- For Pythonistas, I wrote a similar tool called [konch](https://github.com/sloria/konch)
