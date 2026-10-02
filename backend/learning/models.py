from django.db import models


class LearningResource(models.Model):
    resource_id = models.AutoField(primary_key=True)

    skill = models.ForeignKey(
        'skills.Skill',
        on_delete=models.DO_NOTHING,
        db_column='skill_id'
    )

    title = models.CharField(max_length=200)

    description = models.TextField(
        blank=True,
        null=True
    )

    resource_type = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    resource_url = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    difficulty = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    estimated_hours = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'learning_resources'

    def __str__(self):
        return self.title


class LearningProgress(models.Model):
    progress_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.DO_NOTHING,
        db_column='user_id'
    )

    resource = models.ForeignKey(
        LearningResource,
        on_delete=models.DO_NOTHING,
        db_column='resource_id'
    )

    progress_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    started_at = models.DateTimeField(
        blank=True,
        null=True
    )

    completed_at = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'learning_progress'
        unique_together = (('user', 'resource'),)