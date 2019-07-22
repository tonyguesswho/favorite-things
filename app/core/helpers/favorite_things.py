from django.db.models import F
from core.models import Favorite


def adjust_ranking(request, data, instance=None):
    """adjust favorite thing ranks"""

    if(request.method == 'DELETE'):
        Favorite.objects.filter(
                ranking__gt=instance.ranking,
                user_id=request.user.id,
                category_id=instance.category).update(ranking=F('ranking') - 1)
    elif data.get('ranking', None):
        if instance and instance.ranking == data['ranking']:
            pass
        else:
            ranking = data['ranking']
            category_in_data = data.get('category', None)
            category = data['category'] if category_in_data else \
                instance.category
            if(Favorite.objects.filter(
                 ranking=ranking,
                 user_id=request.user.id, category_id=category).count()) > 0:
                if instance:
                    if instance.ranking < data['ranking']:
                        diff_rank = data['ranking'] - instance.ranking
                        Favorite.objects.filter(
                            ranking__gt=instance.ranking,
                            ranking__lt=instance.ranking + (diff_rank + 1),
                            user_id=request.user.id,
                            category_id=category).update(
                                ranking=F('ranking') - 1)
                    if instance.ranking > data['ranking']:
                        diff_rank = instance.ranking - data['ranking']
                        Favorite.objects.filter(
                            ranking__lt=instance.ranking,
                            ranking__gt=instance.ranking - (diff_rank + 1),
                            user_id=request.user.id,
                            category_id=category).update(
                                ranking=F('ranking') + 1)
                else:
                    Favorite.objects.filter(
                        ranking__gte=ranking,
                        user_id=request.user.id,
                        category_id=category).update(ranking=F('ranking') + 1)
