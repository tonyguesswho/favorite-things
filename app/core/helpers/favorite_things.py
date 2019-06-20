from django.db.models import F
from core.models import Favorite


def adjust_ranking(request, data, instance=None):

    if data.get('ranking', None):
        if instance and instance.ranking == data['ranking']:
            pass
        else:
            ranking = data['ranking']
            category_in_data = data.get('category', None)
            category = data['category'] if category_in_data else \
                instance.category
            Favorite.objects.filter(
                ranking__gte=ranking,
                user_id=request.user.id,
                category_id=category).update(ranking=F('ranking') + 1)
