class ZendeskModel:
    __dataclass_fields__: dict
    @classmethod
    def get_searchable_fields(cls, sort: bool = True) -> dict: ...

class User(ZendeskModel):
    pass

class Ticket(ZendeskModel):
    pass

class Organization(ZendeskModel):
    pass
