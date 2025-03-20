from __future__ import annotations


import uniserde
import uniserde.compat
from datetime import datetime, timezone
import typing as t
import dataclasses
from bson import ObjectId
import tests.models as models


serde = uniserde.BsonSerde(lazy=False)

value_fresh = models.ChildClass.create_child_variant_1()

value_bson = serde.as_bson(value_fresh)
assert value_bson["type"] == "ChildClass"

value_round_trip = serde.from_bson(
    models.ParentClass,
    value_bson,
)

assert isinstance(value_round_trip, models.ChildClass)
assert value_fresh == value_round_trip

raise SystemExit()


from dataclasses import dataclass
import uniserde
import uniserde.codegen
import uuid
import tests.models
import enum


original = tests.models.ClassWithStaticmethodOverrides.create()


print(f"Original: {original}")

serialized = uniserde.as_bson(original)

print(f"Serialized: {serialized}")

deserialized = uniserde.from_bson(
    type(original),
    serialized,
)

print(f"Deserialized: {deserialized}")
