from django.contrib.auth.mixins import UserPassesTestMixin

def otm(phone , code):
    pass


class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin