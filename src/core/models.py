# -*-coding:utf-8 -*-
'''
Created on 2013-10-25

@author: Danny<manyunkai@hotmail.com>
DannyWork Project
'''

from django.contrib.comments.models import Comment
from django.contrib.comments.managers import CommentManager
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.expressions import F
from django.db.models.signals import pre_delete

from dblog.models import Blog


class DCommentManager(CommentManager):
    def get_comments(self, obj):
        try:
            obj_type = ContentType.objects.get_for_model(obj)
            return self.filter(content_type=obj_type, object_pk=obj.pk,
                               related=None, is_public=True)
        except:
            return []

    def get_target_comment(self, cmt_id):
        try:
            return self.get(id=cmt_id)
        except:
            return None


class DComment(Comment):
    related = models.ForeignKey('DComment', null=True, blank=True, related_name='related_comment')
    mail_reply = models.BooleanField(u'接收回复邮件', default=True)
    objects = DCommentManager()

    def get_replys(self):
        return self.related_comment.all()


def dcomment_pre_delete(sender, **kwargs):
    instance = kwargs.get('instance')
    obj = instance.content_object
    if isinstance(obj, Blog):
        obj.comment_count = F('comment_count') - 1
        obj.save()

pre_delete.connect(dcomment_pre_delete, sender=DComment)
