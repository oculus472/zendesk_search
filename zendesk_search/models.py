from dataclasses import dataclass

__all__ = ["ZendeskModel", "User", "Ticket", "Organization"]


@dataclass(frozen=True)
class ZendeskModel:
    _id: str
    url: str
    external_id: str
    created_at: str
    tags: list[str]

    @classmethod
    def get_searchable_fields(cls, sort=True):
        fields = list(cls.__dataclass_fields__.keys())
        if sort:
            fields.sort()
        return fields


@dataclass(frozen=True)
class User(ZendeskModel):
    name: str
    alias: str
    active: bool
    verified: bool
    shared: bool
    locale: str


@dataclass(frozen=True)
class Ticket(ZendeskModel):
    type: str
    subject: str
    description: str
    priority: str
    status: str
    submitter_id: int
    organization_id: int
    has_incidents: bool
    due_at: str
    via: str


@dataclass(frozen=True)
class Organization(ZendeskModel):
    name: str
    domain_names: list[str]
    details: str
    shared_tickets: bool
