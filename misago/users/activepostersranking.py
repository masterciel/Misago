from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone

from misago.categories.models import Category
from misago.conf import settings

from .models import ActivityRanking


UserModel = get_user_model()


def get_active_posters_ranking():
    users = []

    queryset = ActivityRanking.objects.select_related("user", "user__rank")
    for ranking in queryset.order_by("-score"):
        ranking.user.score = ranking.score
        users.append(ranking.user)

    return {"users": users, "users_count": len(users)}


def build_active_posters_ranking():
    tracked_period = settings.MISAGO_RANKING_LENGTH
    tracked_since = timezone.now() - timedelta(days=tracked_period)

    ActivityRanking.objects.all().delete()

    ranked_categories = []
    for category in Category.objects.all_categories():
        ranked_categories.append(category.pk)

    queryset = (
        UserModel.objects.filter(
            is_active=True,
            post__posted_on__gte=tracked_since,
            post__category__in=ranked_categories,
        )
        .annotate(score=Count("post"))
        .filter(score__gt=0)
        .order_by("-score")
    )[: settings.MISAGO_RANKING_SIZE]

    new_ranking = []
    for ranking in queryset.iterator():
        new_ranking.append(ActivityRanking(user=ranking, score=ranking.score))
    ActivityRanking.objects.bulk_create(new_ranking)
