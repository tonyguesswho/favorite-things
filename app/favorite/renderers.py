from core.renderers import CoreJSONRenderer


class FavoriteJsonRenderer(CoreJSONRenderer):
    object_label = 'favorite'
    pagination_object_label = 'favorites'
    pagination_count_label = 'favoritesCount'
