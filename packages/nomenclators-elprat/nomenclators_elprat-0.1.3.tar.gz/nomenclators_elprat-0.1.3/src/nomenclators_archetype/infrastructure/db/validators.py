"""
----------------------------------------------------------------------------------------------------
Written by:
  - Yovany Dominico Girón (y.dominico.giron@elprat.cat)

for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""
from typing import TypeVar, Protocol, Optional, Union

from nomenclators_archetype.domain.commons import NomenclatorId
from nomenclators_archetype.domain.commons import BaseSimpleNomenclator
from nomenclators_archetype.domain.validator.commons import BaseValidator

I = TypeVar('I', bound=NomenclatorId)  # Identifier class representation
S = TypeVar('S', bound=BaseSimpleNomenclator)  # Service class representation


class EntityValidator(BaseValidator, Protocol[I, S]):
    """EntityValidator class"""

    @classmethod
    def validate_foreign_key(cls, identifier: I, service: S) -> Optional[Union[str, dict]]:
        """Validate the foreign key"""
        item = service.get_item_by_id(identifier)
        return {'identifier': identifier, 'message': f"no se encuentra en la entidad {service.__class__}."} if item is None else None

    @classmethod
    def validate_unique_element(cls, service: S, spec: dict) -> Optional[Union[str, dict]]:
        """Validate the unique element"""

        items = service.find_by_spec(spec)
        return {"identifier's": ', '.join(spec.keys), 'message': f"se encuentran en la entidad {service.__class__} con los valores {', '.join(spec.values)}."} if items is None else None
