from core.renderers import CoreJSONRenderer


class CategoryJsonRenderer(CoreJSONRenderer):
    object_label = 'category'
    pagination_object_label = 'categories'
    pagination_count_label = 'categoriesCount'
