from __future__ import unicode_literals

import sys

from lib2to3.pytree import Node, Leaf
from lib2to3.fixer_util import token, syms

from yapf.yapflib import pytree_utils

from django.utils import six

from .config import yapf as yapf_config


MAX_LINE_LENGTH = yapf_config.getint('style', 'column_limit') + 1


def fix_formatting(filesource):
    if not ('{'  in filesource and ('[' in filesource or '(' in filesource)):
        return filesource

    tree = pytree_utils.ParseCodeToTree(filesource)
    for node in tree.children:
        walk_tree(node, node.children)
    return six.text_type(tree)


def walk_tree(node, children):
    for item in children:
        if item.type == syms.dictsetmaker:
            walk_dict_tree(item, item.children)
        else:
            walk_tree(item, item.children)


def walk_dict_tree(node, children):
    for item in children:
        prev = item.prev_sibling
        if isinstance(prev, Leaf) and prev.value == ':':
            if isinstance(item, Leaf):
                if six.text_type(item).startswith("\n"):
                    item.replace(Leaf(
                        item.type,
                        item.value,
                        prefix=' ',
                    ))
            elif six.text_type(item).strip()[0] in ('[', '{'):
                walk_tree(item, item.children)
            else:
                walk_dedent_tree(item, item.children)


def walk_dedent_tree(node, children):
    force_split_next = False
    for item in children:
        prev = item.prev_sibling
        if not prev:
            if isinstance(item, Leaf) and six.text_type(item).startswith("\n"):
                prev = node.prev_sibling
                next = node.next_sibling
                final_length = 0

                if prev and "\n" not in six.text_type(node).strip():
                    final_length = prev.column + len(six.text_type(node).strip()) + 3

                item.replace(Leaf(
                    item.type,
                    item.value,
                    prefix=' ',
                ))

                if final_length and final_length > MAX_LINE_LENGTH:
                    # tell next call to walk_dedent_tree_node that we need
                    # different stringformat tactic
                    force_split_next = True
        elif isinstance(item, Node):
            for subitem in item.children[1:]:
                walk_dedent_tree_node(subitem, subitem.children, force_split_next)
                force_split_next = False


def walk_dedent_tree_node(node, children, force_split_next=False):
    if six.text_type(node).startswith("\n"):
        if isinstance(node, Leaf):
            prev = node.prev_sibling
            is_followup = prev and prev.type == token.STRING and node.type == token.STRING
            if is_followup:
                new_value = node.value
                new_prefix = "\n%s" % (' ' * (len(prev.prefix.lstrip("\n")) / 4 * 4))

                # insert linebreak after last string in braces, so its closing brace moves to new line
                if not node.next_sibling:
                    closing_bracket = node.parent.parent.children[-1]
                    if not six.text_type(closing_bracket).startswith("\n"):
                        new_value = "%s\n%s" % (node.value, (' ' * ((len(prev.prefix.lstrip("\n")) / 4 - 1) * 4)))

                node.replace(Leaf(
                    node.type,
                    new_value,
                    prefix=new_prefix,
                ))
            else:
                node.replace(Leaf(
                    node.type,
                    node.value,
                    prefix=node.prefix[:-4],
                ))
        else:
            for item in children:
                walk_dedent_tree_node(item, item.children)
    elif isinstance(node, Leaf):
        if node.type == token.STRING:
            strings_tuple = node.parent.parent

            # compute indent
            if force_split_next:
                container = strings_tuple.parent.children[0]
            else:
                container = strings_tuple.parent.parent.children[0]
            while isinstance(container, Node):
                container = container.children[0]
            indent = container.column + 4

            prev = node.prev_sibling
            next = node.next_sibling

            is_opening = prev is None and six.text_type(strings_tuple).strip()[0] == '('
            has_followup = next and next.type == token.STRING

            if is_opening and has_followup:
                node.replace(Leaf(
                    node.type,
                    node.value,
                    prefix="\n%s" % (' ' * indent),
                ))
            elif force_split_next:
                node.replace(Leaf(
                    node.type,
                    "%s\n%s" % (node.value, (' ' * (indent - 4))),
                    prefix="\n%s" % (' ' * indent),
                ))
    else:
        for item in children:
            walk_dedent_tree_node(item, item.children)

