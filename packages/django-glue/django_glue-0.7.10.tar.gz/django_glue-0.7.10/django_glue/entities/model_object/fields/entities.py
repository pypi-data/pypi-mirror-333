from dataclasses import dataclass, field
from typing import Any, Union

from django_glue.entities.model_object.fields.seralizers import serialize_field_value
from django_glue.form.field.entities import GlueFormField


@dataclass
class GlueModelFieldMeta:
    type: str
    name: str
    glue_field: GlueFormField

    def to_dict(self) -> dict:
        return {
            'type': self.type,
            'name': self.name,
            'glue_field': self.glue_field.to_dict(),
        }


@dataclass
class GlueModelField:
    name: str
    value: Any
    _meta: Union[GlueModelFieldMeta, dict] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'value': serialize_field_value(self),
            '_meta': self._meta.to_dict()
        }


@dataclass
class GlueModelFields:
    fields: list[GlueModelField] = field(default_factory=list)

    def __iter__(self):
        return self.fields.__iter__()

    def to_dict(self):
        return {field.name: field.to_dict() for field in self.fields}
