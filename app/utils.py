def get_item(ancestor, selector, attribute=None, return_list=False):
    """Return a string (or a list of strings) contained in an HTML tag passed as a parameter."""
    try:
        if return_list:
            return [item.get_text().strip() for item in ancestor.select(selector)]
        if attribute:
            return ancestor.select_one(selector)[attribute]
        return ancestor.select_one(selector).get_text().strip()
    except (AttributeError, TypeError):
        return None
