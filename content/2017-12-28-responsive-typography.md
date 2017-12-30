title: Responsive Typography Using Modern CSS
tags: css, postcss, typography
description: A guide to implementing responsive type scales.
slug: responsive-typography
category: programming
status: draft


Choosing type sizes for a website can be daunting. Heading and
paragraph sizes have drastic consequences over the layout and
legibility of a page. Thankfully, we have *modular scales* to guide us.

> A modular scale is a sequence of numbers that relate to one another in a meaningful way.
<cite>Tim Brown, <a href="http://alistapart.com/article/more-meaningful-typography">More Meaningful Typography</a></cite>

Modular scales are used in typography to create visual hierarchy and
harmonious proportions. They provide a set of numbers to use
as guidelines for font sizes and spacing.

<figure>
  <img alt="An example modular scale" src="https://user-images.githubusercontent.com/2379650/34426269-9cc0d7ca-ec02-11e7-98d0-510b719eb2db.png" >
  <figcaption>
    A modular scale in typography
  </figcaption>
</figure>

Implementing a modular scale in the context of the web typically involves manual calculation
and hand-coding values in different places in your CSS. Extra care must
be taken to maintain balanced proportions on all screen sizes.

We can take advantage of new CSS features to make it easier to design with modular scales in a responsive website.
We'll start by using custom properties and
`calc()` to dynamically compute the values for a modular scale.
Then we'll change the scale based on viewport size,
using media queries and the `media()` function.

## Recommended: PostCSS and cssnext

In order to retain browser compatibility when using modern CSS syntax,
I recommend using PostCSS with the cssnext plugin.

<aside>
<p><a href="http://postcss.org/">PostCSS</a> is a JavaScript CSS parser that powers a variety of
plugins that can
transform your CSS.</p>

<p><a href="http://cssnext.io/">cssnext</a> is a PostCSS plugin that transforms syntax and functions
from CSS spec drafts into more compatible CSS.</p>

</aside>

A minimal `postcss.config.js` will look like this:

```javascript
// postcss.config.js
module.exports = {
  plugins: [
    require('postcss-cssnext'),
  ],
};
```

See the [PostCSS documentation](https://github.com/postcss/postcss#usage) for instructions on how to integrate PostCSS with your preferred build tool (webpack, gulp, etc.).

## Implementing a scale

Start by defining your fonts and type scale as [custom properties][custom-properties].
Use [`calc()`](https://developer.mozilla.org/en-US/docs/Web/CSS/calc) to calculate varying
powers of your chosen ratio. We'll use a ratio of 1.414 (the *augmented fourth*, in musical terms)
for the following example.

A few guidelines regarding units:

* **Use percentages for base font sizes.** Percent units respect the
browser's text size setting. See [CSS Font-Size: em vs. px vs. pt vs. percent](https://kyleschaeffer.com/development/css-font-size-em-vs-px-vs-pt-vs/) for more information.
* **Use `em` units for heading sizes and spacing.** `em` is a relative unit,
  so it scales according to the base font size. See [Type Study: Sizing the Legible Letter](http://blog.typekit.com/2011/11/09/type-study-sizing-the-legible-letter/)
  to learn more about using `em` units.

<aside>
  We'll only style h1, h2, h3, p, and small in the following examples for brevity.
  If you make use of all the heading tags, you may need to define more steps in
  the scale.
</aside>

```css
:root {
  /* Font faces */
  --headerFont: 'Helvetica Neue', sans-serif;
  --bodyFont: 'Georgia', serif;
  --fontColor: hsla(0, 0%, 0%, 0.8);
  --lineHeight: 1.5;
  --baseFontSize: 112.5%;  /* 18px */
  /* Type scale */
  --ratio: 1.414;  /* Augmented fourth */
  /* Each step of the scale is a power
     of --ratio
  */
  --stepUp1: calc(1em * var(--ratio));
  --stepUp2: calc(var(--stepUp1) *
                  var(--ratio));
  --stepUp3: calc(var(--stepUp2) *
                  var(--ratio));
  --stepDown1: calc(1em /
                    var(--ratio));
}
```

You can then reference these variables when setting your base fonts.


```css
html {
  font-size: var(--baseFontSize);
  color: var(--fontColor);
  line-height: var(--lineHeight);
  font-family: var(--bodyFont);
}

h1,
h2,
h3 {
  margin: var(--stepUp1) 0 0.5em;
  font-family: var(--headerFont);
  line-height: 1.2;
}

h1 {
  font-size: var(--stepUp3);
}

h2 {
  font-size: var(--stepUp2);
}

h3 {
  font-size: var(--stepUp1);
}

small {
  font-size: var(--stepDown1);
}
```

We get the following result:

<p data-height="480" data-theme-id="0" data-slug-hash="KZNWWj" data-default-tab="result" data-user="sloria" data-embed-version="2" data-pen-title="Type Scaling using cssnext" class="codepen">See the Pen <a href="https://codepen.io/sloria/pen/KZNWWj/">Type Scaling using cssnext</a> by Steven Loria (<a href="https://codepen.io/sloria">@sloria</a>) on <a href="https://codepen.io">CodePen</a>.</p>
<script async src="https://production-assets.codepen.io/assets/embed/ei.js"></script>

The result looks okay, **unless you are viewing this post on your phone…**

## Problems on mobile

The scale used above works well for wide screen viewing.
However, **a ratio that's appropriate for desktop or laptop viewing is unlikely to work
on smaller screens.**

Jason Pamental explains why:

 > As the screen size shrinks and fewer elements are visible, the relative scale between elements becomes exaggerated.
 <cite>Jason Pamental, <a href="https://typecast.com/blog/a-more-modern-scale-for-web-typography">A More Modern Scale for Web Typography</a></cite>

Consequently, we have disproportionately large
headings on small screen sizes.

<figure>
  <img alt="Non-responsive scale" src="https://user-images.githubusercontent.com/2379650/34420634-ac4bdb60-ebd8-11e7-81c6-76178f577047.png" >
  <figcaption>
    A modular scale for large screens will not work for smaller devices.
  </figcaption>
</figure>


## Making it responsive

On smaller viewports, there are fewer visual elements competing for
attention. Therefore, we can reduce the base font size and have less contrast between heading
sizes.

For our example, let's use the following values:

* Screens **smaller than 36em**: base font size of 100% (16px), ratio of 1.2
* Screens **between 36 em and 48em**: base font size of 112.5% (18px), ratio of 1.2
* Screens **larger than 48em**: base font size of 112.5% (18px), ratio of 1.414

<figure>
  <img alt="Different scales on different devices" src="https://user-images.githubusercontent.com/2379650/34420563-46f448f6-ebd8-11e7-8ee6-8c329dc37df8.png">
  <figcaption>
    Use different scales and base font sizes for different viewports.
  </figcaption>
</figure>

We'll go over two ways to implement the desired result. First, we'll use
media queries. Then we'll use the `media()` function to make the code
more concise.

## Using media queries


Since we have two type scale ratios, we'll write two sets of
variables: one for small and
medium screens and one for large screens. We'll also define two base font sizes.

```css
:root {
   /* Base sizes */
  --baseFontSizeSm: 100%; /* 16px */
  --baseFontSizeMd: 112.5%; /* 18px */
  /* Type scale on smaller screens */
  --ratioSm: 1.2;  /* Minor third */
  --stepUp1Sm: calc(1em * var(--ratioSm));
  --stepUp2Sm: calc(var(--stepUp1Sm) *
                    var(--ratioSm));
  --stepUp3Sm: calc(var(--stepUp2Sm) *
                    var(--ratioSm));
  --stepDown1Sm: calc(1em /
                      var(--ratioSm));
  /* Type scale on larger screens */
  --ratioLg: 1.414;  /* Augmented fourth */
  --stepUp1Lg: calc(1em * var(--ratioLg));
  --stepUp2Lg: calc(var(--stepUp1Lg) *
                    var(--ratioLg));
  --stepUp3Lg: calc(var(--stepUp2Lg) *
                    var(--ratioLg));
  --stepDown1Lg: calc(1em /
                      var(--ratioLg));
}
```

Next, we'll write the two break points to use in our media queries.

**Use `em` units for media queries because they behave the most consistently across
browsers.** See [PX, EM or REM Media Queries?](https://zellwk.com/blog/media-query-units/)
for a comparison of the units.

We'll define our break points as [custom media][custom-media-queries] (another cssnext feature) so that we can refer to them
by name.

<aside>
  cssnext allows you to use ">=" and "<=" in media queries, which are more readable than
  "min-" and "max-."
</aside>



```css
@custom-media --break-md (width >= 36em);
@custom-media --break-lg (width >= 48em);
```

The base font size should increase at the "medium" break point.

```css
html {
  font-size: var(--baseFontSizeSm);
  color: var(--fontColor);
  line-height: var(--lineHeight);
  font-family: var(--bodyFont);

  @media (--break-md) {
    font-size: var(--baseFontSizeMd);
  }
}
```

The ratio should increase at the "large" break point, so we refer to
the large scale steps in our media queries.

```css
h1 {
  font-size: var(--stepUp3Sm);
  @media (--break-lg) {
    font-size: var(--stepUp3Lg);
  }
}

h2 {
  font-size: var(--stepUp2Sm);
  @media (--break-lg) {
    font-size: var(--stepUp2Lg);
  }
}

h3 {
  font-size: var(--stepUp1Sm);
  @media (--break-lg) {
    font-size: var(--stepUp1Lg);
  }
}

small {
  font-size: var(--stepDown1Sm);
  @media (--break-lg) {
    font-size: var(--stepDown1Lg);
  }
}
```

<p data-height="480" data-theme-id="0" data-slug-hash="GyNxbM" data-default-tab="result" data-user="sloria" data-embed-version="2" data-pen-title="Responsive modular scale using cssnext" class="codepen">See the Pen <a href="https://codepen.io/sloria/pen/GyNxbM/">Responsive modular scale using cssnext</a> by Steven Loria (<a href="https://codepen.io/sloria">@sloria</a>) on <a href="https://codepen.io">CodePen</a>.</p>
<script async src="https://production-assets.codepen.io/assets/embed/ei.js"></script>

The font sizes properly adjust to the viewport size. Much better!

This approach is certainly more convenient than hand-calculating values for our scales,
but it still requires at least one media query every time
we refer to a step in the scale.

We can make the code even more concise with the `media()` function,
which we'll dig into next.

## Using the `media()` function

Rather than defining separate sets of variables for each modular scale,
we can use the `media()` function ([spec][media-expressions]) to assign
responsive values to our scale properties.

This feature requires the [postcss-media-fn](https://github.com/jonathantneal/postcss-media-fn) plugin in addition to cssnext.
Install it with npm or yarn and add it to your `postcss.config.js`.

```
npm install postcss-media-fn
```

```javascript
// postcss.config.js
module.exports = {
  plugins: [
    require('postcss-cssnext'),
    require('postcss-media-fn'),
  ],
};
```

Use the `media()` function when defining your type scale variables.
Each step of the scale combines the type scale calculations for each
break point.

A step in our scale will look like this:

```js
--stepUp1: media(
  calc(1em * var(--ratioSm)),
  (min-width: 48em) calc(1em * var(--ratioLg))
);
```

Let's break it down.

* The default size for the first step of the scale is `1em` × 1.2 (our smaller ratio).
* Beyond `48em` (our "large" break point), the first step is `1em` × 1.414 (our larger ratio).

Here is the full scale using `media()`:

```css
:root {
  /* Break points */
  --minMd: 36em;
  --minLg: 48em;

  /* Ratio on smaller screens */
  --ratioSm: 1.2; /* Minor third */

  /* Ratio on larger screens */
  --ratioLg: 1.414; /* Augmented fourth */

  /* Type scale */
  --stepUp1: media(
    calc(1em * var(--ratioSm)),
    (min-width: var(--minLg)) calc(1em * var(--ratioLg))
  );
  --stepUp2: media(
    calc(1em * var(--ratioSm) * var(--ratioSm)),
    (min-width: var(--minLg)) calc(1em * var(--ratioLg) * var(--ratioLg))
  );
  --stepUp3: media(
    calc(1em * var(--ratioSm) * var(--ratioSm) * var(--ratioSm)),
    (min-width: var(--minLg)) calc(1em * var(--ratioLg) * var(--ratioLg) * var(--ratioLg))
  );
  --stepDown1: media(
    calc(1em / var(--ratioSm)),
    (min-width: var(--minMd)) calc(1em / var(--ratioLg))
  );
}
```

With this setup, **we no longer need to include media queries when
referring to our scale.**


```css
h1 {
  font-size: var(--stepUp3);
}

h2 {
  font-size: var(--stepUp2);
}

h3 {
  font-size: var(--stepUp1);
}

small {
  font-size: var(--stepDown1);
}
```

This approach requires a little more setup, but it results in tidier
code when you use your scale in many places.

## In summary…

Follow these guidelines when designing with modular type scales on
the web:

* Use custom properties and `calc()` to dynamically scale your font sizes according to a modular scale.
* Use percent units for base font sizes. Use `em` for sizing text and media queries.
* Use different scales for different viewport sizes. The smaller the viewport, the smaller the type scale ratio can be.
* Use media queries or the `media()` function to change the ratio and base font size based on the viewport.

## Related links

* [Typographic Scale](http://spencermortensen.com/articles/typographic-scale/) - Primer on modular scales
* [ModularScale.com](http://www.modularscale.com/) and [Type-Scale.com](http://type-scale.com/) - Online tools for visualizing modular type scales
* [Responsive Modular Scale](https://zellwk.com/blog/responsive-modular-scale/) - Different approaches for using modular scales on responsive web sites
* [A More Modern Scale for Web Typography](https://typecast.com/blog/a-more-modern-scale-for-web-typography) - On using different proportions based on the viewport size

[custom-properties]: https://developer.mozilla.org/en-US/docs/Web/CSS/--*
[calc]: https://developer.mozilla.org/en-US/docs/Web/CSS/calc
[custom-media-queries]: https://drafts.csswg.org/mediaqueries-5/#custom-mq
[media-expressions]: https://jonathantneal.github.io/media-expressions-spec/
