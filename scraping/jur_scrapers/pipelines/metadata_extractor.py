# -*- coding: utf-8 -*-

from extraction import MetadataExtractor


class MetadataExtractorPipeline(object):
    metadata_extractor = MetadataExtractor()

    def process_item(self, item, spider):
        return self.metadata_extractor.extract(item)
