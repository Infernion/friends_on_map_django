"""Django ORM models for Social Auth"""
import base64
import six

from social.storage.base import UserMixin, AssociationMixin, NonceMixin, \
                                CodeMixin, BaseStorage


class DjangoUserMixin(UserMixin):
    pass

class DjangoNonceMixin(NonceMixin):
    pass

class DjangoCodeMixin(CodeMixin):
    pass

class BaseDjangoStorage(BaseStorage):
    user = DjangoUserMixin
    code = DjangoCodeMixin

user = DjangoUserMixin()
user.set_extra_data(extra_data={'test':'test2'})
