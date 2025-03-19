from typing import Optional
from pydantic import BaseModel
from typing import Optional

from pydantic import BaseModel


class Filter(BaseModel):
    field: Optional[str] = None
    lookup: Optional[str] = None
    help_text: Optional[str] = None

    def to_str(self) -> str:
        data = self.model_dump()
        sorted_items = [('id', data.pop('id'))] if 'id' in data else []
        sorted_items += sorted(data.items())
        fields = "\n    ".join(f"{key}={value}" for key, value in sorted_items)

        return f"<{self.__class__.__name__}\n    {fields}\n>"

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        id = getattr(self, 'id', None)
        name = getattr(self, 'name', None)

        if id and name:
            return f"<{self.__class__.__name__} id={self.id} name={self.name}>"
        if id:
            return f"<{self.__class__.__name__} id={self.id}>"
        return f"<{self.__class__.__name__}>"