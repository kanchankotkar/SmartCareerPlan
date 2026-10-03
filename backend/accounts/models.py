from django.db import models


class User(models.Model):

    user_id = models.AutoField(
        primary_key=True
    )

    full_name = models.CharField(
        max_length=150
    )

    email = models.CharField(
        max_length=150,
        unique=True
    )

    password_hash = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    education = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    experience_years = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True
    )

    target_role = models.ForeignKey(
        'careers.JobRole',
        on_delete=models.DO_NOTHING,
        db_column='target_role_id',
        blank=True,
        null=True,
        related_name='users'
    )

    is_admin = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        blank=True,
        null=True
    )

    updated_at = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.email