from django.db import models


class JobRole(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    experience_level = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'job_roles'

    def __str__(self):
        return self.role_name


class JobRoleSkill(models.Model):
    role_skill_id = models.AutoField(primary_key=True)

    role = models.ForeignKey(
        JobRole,
        on_delete=models.DO_NOTHING,
        db_column='role_id'
    )

    skill = models.ForeignKey(
        'skills.Skill',
        on_delete=models.DO_NOTHING,
        db_column='skill_id'
    )

    importance = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    minimum_level = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'job_role_skills'
        unique_together = (('role', 'skill'),)