class Strings:
    def __init__(self) -> None:
        pass

    def location_coordenates(self, latitude, longitude):
        return str(latitude)+','+str(longitude)

    def location_message(self, quote_id, message:str):
        return quote_id+message