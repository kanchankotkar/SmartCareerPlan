from django.db import models


class Skill(models.Model):
    skill_id = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'skills'

    def __str__(self):
        return self.skill_name


class UserSkill(models.Model):
    user_skill_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.DO_NOTHING,
        db_column='user_id'
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.DO_NOTHING,
        db_column='skill_id'
    )

    skill_level = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    years_experience = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True
    )

    is_verified = models.IntegerField(
        blank=True,
        null=True
    )

    added_at = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'user_skills'
        unique_together = (('user', 'skill'),)