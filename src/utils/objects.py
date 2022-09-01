class Objects:
    def __init__(self) -> None:
        pass

    def object_coordinates(self, latitude, longitude):
        return {'latitude': str(latitude), 'longitude': str(longitude)}

    def object_taxes(self, tax_min, tax_max, tax_extra):
        return {'tax_min': tax_min, 'tax_max': tax_max, 'tax_extra': tax_extra}
