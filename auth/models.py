from social.storage.base import UserMixin, AssociationMixin, NonceMixin, \
                                CodeMixin, BaseStorage
from urllib import urlopen

class UserModel(UserMixin):
	def add_friends(self):
		# friends = 'https://api.vk.com/method/friends.get?uid=%s&cids=%s&fields=%s&access_token=%s' % (self.u)
		self.extra_data['test'] = 'test'

class NonceModel(NonceMixin):
	pass

class AssociationModel(AssociationMixin):
	pass

class CodeModel(CodeMixin):
	pass

class StorageImlpementation(BaseStorage):
    user = UserModel
    nonce = NonceModel
    association = AssociationModel
    code = CodeModel
    
    @classmethod
    def is_integrity_error(cls, exception):
        """Check if given exception flags an integrity error in the DB"""
        raise NotImplementedError('Implement in subclass')