title: Building a Dashboard for a Python Package
tags: python, marshmallow
description: Why and how I built a dashboard for marshmallow.
category: programming
status: published

I made a simple dashboard for visualizing marshmallow PyPI downloads.

<figure>
  <a href="http://marshmallow.sloria.io/">
  <img alt="marshmallow dashboard" height="250" src="https://user-images.githubusercontent.com/2379650/64126549-32986e00-cd7c-11e9-92df-8c3b5bb391b4.png">
  </a>
</figure>

## Why

While maintaining marshmallow, I found myself running one-off queries against [PyPI's BigQuery dataset](https://packaging.python.org/guides/analyzing-pypi-package-downloads/) to answer some recurring questions:

- How many marshmallow users are using Python 2 vs Python 3?
- Can we drop support for a minor Python version without pissing too many users off?
- Are users migrating to marshmallow 3?
- How long should we support old marshmallow versions?

Executing and modifying BigQuery queries by hand quickly became tedious.

## How

I run a [daily scheduled query](https://cloud.google.com/bigquery/docs/scheduling-queries) on BigQuery that subsets the PyPI dataset with the specific data that I need. This keeps my BigQuery usage well within the limits of the free tier.

<figure>
  <img alt="Scheduled queries" height="250" src="https://user-images.githubusercontent.com/2379650/64125816-645c0580-cd79-11e9-858f-6bda4f33d12b.png">
  <figcaption>
    BigQuery's scheduled queries UI
  </figcaption>
</figure>

The query starts with a CTE that selects the date, Python major and minor versions, marshmallow major and minor versions, and platform.

```sql
WITH
  dls AS (
  SELECT
    DATE_SUB(DATE(@run_time), INTERVAL 1 DAY) AS date,
    file.project AS package,
    details.installer.name AS installer,
    -- Full python version
    details.python AS python_version,
    -- Python major version
    CAST(SPLIT(details.python, '.')[
    OFFSET
      (0)] AS string) AS python_major,
    -- Python minor version
    CAST(CONCAT(SPLIT(details.python, '.')[
      OFFSET
        (0)],'.',SPLIT(details.python, '.')[
      OFFSET
        (1)]) AS string) AS python_minor,
    -- Full marshmallow version
    file.version AS marshmallow_version,
    -- marshmallow major version
    CAST(SPLIT(file.version, '.')[
    OFFSET
      (0)] AS string) AS marshmallow_major,
    -- Platform
    details.system.name AS system
  FROM
    `the-psf.pypi.downloads*`
  WHERE
    -- Past day
    _TABLE_SUFFIX = FORMAT_DATE('%Y%m%d', DATE_SUB(DATE(@run_time), INTERVAL 1 DAY))
    AND file.project = 'marshmallow'
    -- Exclude mirrors
    AND details.installer.name NOT IN ("bandersnatch",
      "z3c.pypimirror",
      "Artifactory",
      "devpi")
    AND details.python IS NOT NULL )
-- ...
```

Then the query groups the download counts by category:

- Python major version
- Python minor version
- marshmallow major version
- marshmallow minor version
- Python minor version x marshmallow major version

```sql
-- WITH dls AS ...
  -- Python 2 vs 3
  SELECT
    date,
    'python_major' AS category_label,
    python_major AS category_value,
    COUNT(*) AS downloads
    FROM
      dls
    GROUP BY
      date,
      package,
      category_value
  UNION ALL
  -- Python minor versions
  SELECT
    date,
    'python_minor' AS category_label,
    python_minor AS category_value,
    COUNT(*) AS downloads
  FROM
    dls
  GROUP BY
    date,
    package,
    category_value
  UNION ALL
  -- marshmallow major version
  SELECT
    date,
    'marshmallow_major' AS category_label,
    marshmallow_major AS category_value,
    COUNT(*) AS downloads
  FROM
    dls
  WHERE
    marshmallow_major IN ('2', '3')
  GROUP BY
    date,
    package,
    category_value
  UNION ALL
  -- marshmallow minor version
  SELECT
    date,
    'marshmallow_version' AS category_label,
    marshmallow_version AS category_value,
    COUNT(*) AS downloads
  FROM
    dls
  WHERE marshmallow_major IN ('2', '3')
  GROUP BY
    date,
    package,
    category_value
  UNION ALL
  -- Python minor version x marshmallow major version
  SELECT
    date,
    'combined' AS category_label,
    CAST(CONCAT('py', python_minor, '-', 'marshmallow', marshmallow_major) AS string) AS category_value,
    COUNT(*) AS downloads
  FROM
    dls
  WHERE
    marshmallow_major IN ('2', '3')
  GROUP BY
    date,
    package,
    category_value
```

There is no way to directly control for downloads on CI servers. One solution is to exclude downloads on Linux and assume that downloads on Windows and macOS machines are a representative sample of local development installations.

To achieve this, the query includes duplicates of the above `SELECT`s with an additional `WHERE system != "Linux"` clause.

```sql
    -- ... Same as above, excluding Linux downloads
    SELECT
      date,
      'python_major' AS category_label,
      CONCAT(python_major, '-', 'no_linux') AS category_value,
      COUNT(*) AS downloads
    FROM
      dls
    WHERE
      system != "Linux"
    GROUP BY
      date,
      package,
      category_value
    UNION ALL
    -- and so on ...
```

The full query looks is [here](https://gist.github.com/sloria/74a911fa53d4de036c2eca638ece8234). The resulting dataset looks like this:

<figure>
  <img alt="Dataset" height="250" src="https://user-images.githubusercontent.com/2379650/64126217-f44e7f00-cd7a-11e9-94b9-c92dc6e2c33a.png">
  <figcaption>
    Dataset produced by above query
  </figcaption>
</figure>

After backfilling the dataset, I wrote an app to query the dataset and visualize it with [Dash](<[https://dash.plot.ly/](https://dash.plot.ly/)>), a Python framework for creating interactive visualizations.
With pandas at hand to take care of slicing and transforming the dataset, writing the visualization code in Python turned out to be a breeze.

The source code for the Dash app is [here](https://github.com/sloria/marshmallow-dashboard/blob/master/app.py).

## Takeaways

**The majority of marshmallow users are using Python 3.6 and Python 3.7**. Python 3.5 usage is low (even lower than Python 2).

<figure>
  <img alt="Python version usage" height="200" src="https://user-images.githubusercontent.com/2379650/64130101-25847a80-cd8e-11e9-967b-9839627b5723.png">
</figure>

**Users upgrade to new versions quickly**. marshmallow users install the latest point versions of the supported release lines as they're released.

**Don't expect users to use pre-releases**. marshmallow 3 was "release-candidate stable" for several months, and we recommended using v3 for new projects. Even so, v3 remained at < 20% until the stable release.

<figure>
  <img alt="ma 2 vs 3" width="500" src="https://user-images.githubusercontent.com/2379650/64127311-0e8a5c00-cd7f-11e9-89fc-23db66c5321b.png">
</figure>

## Links

- [marshmallow dashboard](https://marshmallow.sloria.io)
- [GitHub repo](https://github.com/sloria/marshmallow-dashboard)
- [Analyzing PyPI package downloads](https://packaging.python.org/guides/analyzing-pypi-package-downloads/)
- [Dash User Guide](https://dash.plot.ly/)
