from __future__ import annotations

from typing import List, Optional, Type

from pydantic import BaseModel, create_model


class ZmpAPIOperation(BaseModel):
    name: str
    description: str
    path: str
    method: str
    path_params: Optional[Type[BaseModel]]
    query_params: Optional[Type[BaseModel]]
    request_body: Optional[Type[BaseModel]]

    @property
    def args_schema(self) -> Type[BaseModel]:
        return self._create_args_schema(
            model_name=f"{self.name}Schema",
            models=[self.path_params, self.query_params, self.request_body],
        )

    def _create_args_schema(
        self,
        *,
        model_name: str,
        models: List[Optional[Type[BaseModel]]],
    ) -> Type[BaseModel]:
        merged_fields = {}
        for model in models:
            if model:
                for field_name, field_info in model.model_fields.items():
                    merged_fields[field_name] = (field_info.annotation, field_info)

        return create_model(model_name, **merged_fields)
