from defpage.lib.util import random_string

class AuthenticatedSessions:

    def __init__(self):
        self._db = {}

    def create(self, user_id, email):
        k = self._create_key()
        self._db[k] = {'user_id':user_id, 'email':email}
        return k

    def get(self, k):
        return self._db.get(k)

    def delete(self, k):
        try:
            del self._db[k]
        except KeyError:
            pass

    def _create_key(self):
        while 1:
            k = random_string(20)
            if k not in self._db:
                return k

authenticated_sessions = AuthenticatedSessions()
