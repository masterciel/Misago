from misago.acl import add_acl

from misago.forums.models import Forum


def get_forums_list(user, parent=None):
    if parent:
        queryset = parent.get_descendants().order_by('lft')
    else:
        queryset = Forum.objects.all_forums()
    queryset_with_acl = queryset.filter(id__in=user.acl['visible_forums'])

    forums_dict = {}
    forums_list = []

    parent_level = parent.level + 1 if parent else 1

    for forum in queryset_with_acl:
        forum.is_read = True
        forum.subforums = []
        forums_dict[forum.pk] = forum
        forums_list.append(forum)

        if forum.level > parent_level:
            forums_dict[forum.parent_id].subforums.append(forum)

    flat_list = []
    for forum in forums_list:
        has_content = (forum.role != "category" or forum.subforums)
        if forum.level == parent_level and has_content:
            flat_list.append(forum)

    add_acl(user, flat_list)
    return flat_list


def get_forum_path(forum):
    forums_dict = Forum.objects.get_cached_forums_dict()

    forum_path = []
    while forum.level > 0:
        forum_path.append(forum)
        forum = forums_dict[forum.parent_id]
    return [f for f in reversed(forum_path)]
