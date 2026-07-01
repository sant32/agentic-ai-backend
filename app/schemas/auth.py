from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class SearchRequest(BaseModel):
    query: str


class SourceResponse(BaseModel):
    file_name: str
    page: int
    score: float
    content: str


class SearchResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]