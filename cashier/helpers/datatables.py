"""Data table helper."""


class DatatablesColumn:
    """Datatables column field."""

    def __init__(self, name, data=None, title=None, orderable=False, searchable=False, tipe='string'):
        """Construct."""
        self.name = name
        self.data = data if data is not None else name
        self.orderable = orderable
        self.searchable = searchable
        self.title = title if title is not None else name.title()
        self.type = tipe

    def to_dict(self):
        """Convert attribute to dictionary."""
        return {
            'name': self.name,
            'data': self.data,
            'title': self.title,
            'type': self.type,
            'orderable': self.orderable,
            'searchable': self.searchable,
        }
