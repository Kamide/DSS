from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    GUEST_USER = 0
    ORDINARY_USER = 1
    SUPER_USER = 2
    COHORTS = (
        (GUEST_USER, 'Guest User'),
        (ORDINARY_USER, 'Ordinary User'),
        (SUPER_USER, 'Super User'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cohort = models.PositiveSmallIntegerField(choices=COHORTS, default=GUEST_USER)
    picture = models.URLField(blank=True)
    interests = models.CharField(max_length=100, blank=True)
    is_locked = models.BooleanField(default=False)
    doc_to_fix = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.user) + ' ' + self.get_cohort() + ' ' + self.picture + ' ' + self.interests

    def make_gu(self):
        self.cohort = self.GUEST_USER

    def make_ou(self):
        self.cohort = self.ORDINARY_USER

    def make_su(self):
        self.cohort = self.SUPER_USER

    def set_cohort(self, value):
        self.cohort = value

    def get_cohort(self):
        return self.COHORTS[self.cohort][1]

    def get_cohort_value(self):
        return self.cohort

    def is_gu(self):
        return self.cohort == self.GUEST_USER

    def is_ou(self):
        return self.cohort == self.ORDINARY_USER

    def is_su(self):
        return self.cohort == self.SUPER_USER

    def has_gu_rights(self):
        return self.cohort >= self.GUEST_USER

    def has_ou_rights(self):
        return self.cohort >= self.ORDINARY_USER

    def has_su_rights(self):
        return self.cohort >= self.SUPER_USER

    def locked(self):
        return self.is_locked
