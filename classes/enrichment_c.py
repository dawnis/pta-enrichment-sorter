from classes.utilities import clean_enrichment_name


class enrichment:
    def __init__(self, enrichment_name, min_size=8, max_size=12):
        # defaults are minimum 8 students and max 12
        self.name = clean_enrichment_name(enrichment_name)
        self.min_size = min_size
        self.max_size = max_size
