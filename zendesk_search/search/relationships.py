collection_relationships = {
    "users": (
        {
            "propogate_field": "assigned_tickets",
            "primary_key": "_id",
            "foreign_key": "assignee_id",
            "collection": "tickets",
        },
        {
            "propogate_field": "submitted_tickets",
            "primary_key": "_id",
            "foreign_key": "submitter_id",
            "collection": "tickets",
        },
        {
            "propogate_field": "organization",
            "primary_key": "organization_id",
            "foreign_key": "_id",
            "collection": "organizations",
        },
    ),
    "tickets": (
        {
            "propogate_field": "submitter",
            "primary_key": "submitter_id",
            "foreign_key": "_id",
            "collection": "users",
        },
        {
            "propogate_field": "assignee",
            "primary_key": "assignee_id",
            "foreign_key": "_id",
            "collection": "users",
        },
        {
            "propogate_field": "organization",
            "primary_key": "organization_id",
            "foreign_key": "_id",
            "collection": "organizations",
        },
    ),
}
