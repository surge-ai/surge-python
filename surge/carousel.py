import json


class Carousel(object):

    def __init__(self, carousel_type=None):
        self.carousel_type = carousel_type

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.to_dict())


class BoundedRoundsCarousel(Carousel):

    def __init__(self, min_rounds_for_carousel=1, max_rounds_for_carousel=1):
        super().__init__(carousel_type="bounded_rounds")
        self.min_rounds_for_carousel = min_rounds_for_carousel
        self.max_rounds_for_carousel = max_rounds_for_carousel


class DataKeyCarousel(Carousel):

    def __init__(self, carousel_data_key=None):
        super().__init__(carousel_type="data_key")
        self.carousel_data_key = carousel_data_key


class OrdinalColumnsCarousel(Carousel):

    def __init__(self, max_rounds_for_carousel=1):
        super().__init__(carousel_type="ordinal_columns")
        self.max_rounds_for_carousel = max_rounds_for_carousel
