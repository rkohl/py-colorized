from __future__ import annotations

from inspect import getmembers
from typing import Any, Protocol, TypeAlias, TypeVar, Union, runtime_checkable

T = TypeVar("T")
Data: TypeAlias = Union[
  dict[str, "Data"],
  list["Data"],
  str,
  int,
  float,
]
"""
 Type alias for data that can be serialized to python types.
 This includes dictionaries, lists, strings, integers, floats, booleans, datetime, and None.
"""


@runtime_checkable
class _Serializabled(Protocol):
  """
  Protocol for objects that can serialize their instance attributes and
  computed properties into a dictionary.
  """

  __dict__: dict[str, Any]

  def serialize(
    self,
    *,
    include_private: bool = False,
    include_properties: bool = True,
  ) -> Data: ...


def serialize_value(value: T) -> Any:
  """
  Recursively convert a value into a serialization-safe representation.
  """

  if value is None or isinstance(value, (str, int, float, bool)):
    return value

  if isinstance(value, dict):
    return {serialize_value(key): serialize_value(item) for key, item in value.items()}

  if isinstance(value, (list, tuple, set, frozenset)):
    return [serialize_value(item) for item in value]

  if isinstance(value, _Serializabled):
    return value.serialize()

  if hasattr(value, "__dict__"):
    return serialize_object(value)

  return value


def serialize_object[T](
  obj: T,
  *,
  include_private: bool = False,
  include_properties: bool = True,
) -> Data:
  """
  Serialize an object's instance attributes and properties.

  Args:
      obj:
          Object to serialize.

      include_private:
          Include names beginning with an underscore.

      include_none:
          Include attributes whose value is None.

      include_properties:
          Include values exposed through @property descriptors.
  """

  result: Data = {}

  for name, value in vars(obj).items():
    # sig = signature(value).return_annotation

    if not include_private and name.startswith("_"):
      continue

    # if not include_errors and callable(value):
    #   continue

    result[name] = serialize_value(value)

  if include_properties:
    for name, descriptor in getmembers(type(obj)):
      if not isinstance(descriptor, property):
        continue

      if not include_private and name.startswith("_"):
        continue

      if name == "serialize":
        continue

      try:
        value = getattr(obj, name)
      except Exception:
        continue

      result[name] = serialize_value(value)

  return result


class Serializable(Protocol):
  """
  Protocol for objects that can serialize their instance attributes and
  computed properties into a dictionary.

  Attributes:
    `serialize`: A property that returns a dictionary representation of the object.
  """

  @property
  def serialize(
    self,
  ) -> Data:
    """
    Return a dictionary representation of the object.
    """
    return serialize_object(
      self,
      include_private=False,
      include_properties=True,
    )
