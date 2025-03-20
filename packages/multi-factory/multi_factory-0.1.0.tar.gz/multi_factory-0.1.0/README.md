# multi_factory

Define a single factory to generate the same data in multiple formats:

- Base (original data as defined on the factory)
- JSON (original data converted into a Python dict that is JSON serialisable)
- Domain (JSON data that is passed through a `marshmallow` schema that validates it and converts it into a domain object like a `@dataclass`)

# Installation

`multi_factory` can be installed using pip (requires Python >=3.10):

```bash
pip install multi-factory
```

# Quick start

With the following setup:

```python
from enum import Enum
from uuid import uuid4, UUID
from datetime import datetime
from dataclasses import dataclass
from marshmallow import Schema, fields


class Gender(Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3


class UserSchema(Schema):
    id = fields.UUID()
    first_name = fields.String()
    last_name = fields.String()
    age = fields.Integer()
    birthday = fields.DateTime()
    gender = fields.Enum(Gender)


@dataclass
class User:
    id: UUID
    first_name: str
    last_name: str
    age: int
    birthday: datetime
    gender: Gender
```

Look at the following example:

```python
import factory


class UserDictFactory(factory.Factory):
    class Meta:
        model = dict

    id = uuid4()
    first_name = "Bob"
    last_name = "Dylan"
    age = 21
    birthday = datetime(year=2000, month=1, day=1, hour=0)
    gender = Gender.MALE


class UserJSONFactory(factory.Factory):
    class Meta:
        model = dict

    id = str(uuid4())
    first_name = "Bob"
    last_name = "Dylan"
    age = 21
    birthday = datetime(year=2000, month=1, day=1, hour=0).isoformat()
    gender = Gender.MALE.name


class UserDomainFactory(factory.Factory):
    class Meta:
        model = User

    id = uuid4()
    first_name = "Bob"
    last_name = "Dylan"
    age = 21
    birthday = datetime(year=2000, month=1, day=1, hour=0)
    gender = Gender.MALE
```

We have to define multiple independent factories to represent the same data in different forms.

With `multi-factory`, we can do the following instead:

```python
import multi_factory import JSONToDomainFactory


class UserFactory(JSONToDomainFactory[User, UserSchema]):
    id = uuid4()
    first_name = "Bob"
    last_name = "Dylan"
    age = 21
    birthday = datetime(year=2000, month=1, day=1, hour=0)
    gender = Gender.MALE
```
