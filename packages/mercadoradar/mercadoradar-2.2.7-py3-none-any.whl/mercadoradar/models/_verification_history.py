from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel


class VerificationHistory(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_deleted: Optional[bool] = None
    deleted_at: Optional[datetime] = None
    id: Optional[int] = None
    user: Optional[Any] = None
    type: Optional[str] = None
    object_type: Optional[str] = None
    object_id: Optional[int] = None
    is_verified: Optional[bool] = None
    reason: Optional[str] = None
    suggestion: Optional[str] = None

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