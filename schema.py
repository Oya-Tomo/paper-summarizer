import pprint
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal


class ElementSchema(BaseModel, extra="forbid"):
    type: Literal["text", "table", "katex"] = Field(
        ..., description="Type of the element"
    )
    content: str = Field(
        ...,
        description="Content of the element. "
        "(text: markdown text that only includes plain/bold/italic text, "
        "table: csv, "
        "katex: latex formula)",
    )


class SectionSchema(BaseModel, extra="forbid"):
    title: str = Field(..., description="Title of the section")
    contents: list[ElementSchema] = Field(..., description="List of section contents")


class DocumentSchema(BaseModel, extra="forbid"):
    sections: list[SectionSchema] = Field(..., description="List of document contents")


if __name__ == "__main__":
    pprint.pprint(DocumentSchema.model_json_schema())
