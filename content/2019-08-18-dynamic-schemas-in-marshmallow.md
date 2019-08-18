title: Dynamic Schemas in marshmallow
tags: python, marshmallow
description: Usage examples for Schema.from_dict.
category: programming
status: published

marshmallow 3 will have a `Schema.from_dict` method that generates a `Schema` class from a dictionary of fields.

```python
from marshmallow import Schema, fields

GistSchema = Schema.from_dict(
    {
        "id": fields.Str(dump_only=True),
        "content": fields.Str(required=True),
    }
)
```

Here's a rundown of a few use cases this API enables.

**Schemas generated at runtime.** Sometimes the shape of your input data is not known ahead of time, and your schema may depend on external sources or user input. In these cases, you can build a dictionary and generate a `Schema` at runtime.

```python
import sys

from marshmallow import Schema, fields

arg, json_input = sys.argv[1], sys.argv[2]

arg_fields = {"f1": fields.Str()}
if arg == "schema1":
    arg_fields.update(
        {
            "f2": fields.Bool(missing=True),
            "f3": fields.Int(default=42),
            "f4": fields.Str(),
        }
    )
elif arg == "schema2":
    arg_fields.update(
        {
            "f5": fields.Str(required=True),
            "f6": fields.Int(required=True),
            "f7": fields.Bool(required=True),
        }
    )

GeneratedSchema = Schema.from_dict(arg_fields)
print(GeneratedSchema().loads(json_input))
```

**Terse schema declarations**. [webargs](https://webargs.readthedocs.io/en/latest/) (validates request objects) and [environs](https://github.com/sloria/environs) (parses/validates environment variables) rely on marshmallow for deserialization. They both build `Schemas` from dictionaries internally without the user having to use `marshmallow.Schema` directly.

```python
# webargs example
from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

app = Flask(__name__)


@app.route("/gists/", methods=["GET", "POST"])
@use_args({"content": fields.Str(required=True)})
def gists(args):
    content = args["content"]
    # ...
```

```python
# environs example
from environs import Env

env = Env()

GH_USER = env.str("GITHUB_USER")
MAX_CONNECTIONS = env.int("MAX_CONNECTIONS", default=100)
```

**Schemas for dataclasses, etc.** Python structures such as dataclasses and `typing.NamedTuple`s store internal dictionary representations, so you can generate marshmallow schemas from them.

```python
import typing
from dataclasses import dataclass


@dataclass
class Owner:
    id: int
    login: str


@dataclass
class Repo:
    id: int
    name: str
    owner: Owner
    topics: typing.List[str]


RepoSchema = Schema.from_dataclass(Repo)
```

`from_dataclass` could be implemented like so:

```python
from dataclasses import is_dataclass, MISSING

from marshmallow import Schema as BaseSchema, fields, missing


class Schema(BaseSchema):
    DATACLASS_TYPE_MAPPING = {**BaseSchema.TYPE_MAPPING, list: fields.List}

    @classmethod
    def from_dataclass(cls, datacls):
        """Generate a Schema from a dataclass."""
        return cls.from_dict(
            {
                name: cls.make_field_for_type(dc_field.type, dc_field.default)
                for name, dc_field in datacls.__dataclass_fields__.items()
            },
            name=f"{datacls.__name__}Schema",
        )

    @classmethod
    def make_field_for_type(cls, type_, default=missing):
        """Generate a marshmallow Field instance from a Python type."""
        if is_dataclass(type_):
            return fields.Nested(cls.from_dataclass(type_))
        # Get marshmallow field class for Python type
        origin_cls = getattr(type_, "__origin__", None) or type_
        FieldClass = cls.DATACLASS_TYPE_MAPPING[origin_cls]
        # Set `required` and `missing`
        required = default is MISSING
        field_kwargs = {"required": required}
        if not required:
            field_kwargs["missing"] = default
        # Handle list types
        if issubclass(FieldClass, fields.List):
            # Construct inner class
            args = getattr(type_, "__args__", [])
            if args:
                inner_type = args[0]
                inner_field = cls.make_field_for_type(inner_type)
            else:
                inner_field = fields.Field()
            field_kwargs["cls_or_instance"] = inner_field
        return FieldClass(**field_kwargs)
```

You can even chain calls to `from_dict` to update generated fields.

```python
RepoSchema = (
    Schema.from_dataclass(Repo)
    .from_dict({"id": fields.Int(dump_only=True)})
)
```
