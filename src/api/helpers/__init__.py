def to_json(rows):
    """Convierte los datos de una lista o consulta a JSON."""
    return [row.get_json() for row in rows]


def paginator_to_json(paginator):
    """Convierte una página y sus items a JSON."""
    return dict(
        has_next=paginator.has_next,
        has_prev=paginator.has_prev,
        items=to_json(paginator.items),
        next_num=paginator.next_num,
        page=paginator.page,
        pages=paginator.pages,
        per_page=paginator.per_page,
        prev_num=paginator.prev_num,
        total=paginator.total,
    )