# Generated by Django 2.1.5 on 2020-03-28 08:34

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import website.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CA",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "caid",
                    models.PositiveIntegerField(blank=True, null=True, unique=True),
                ),
                ("name", models.CharField(max_length=80)),
                ("institute_name", models.CharField(max_length=200)),
                ("points", models.IntegerField(default=0)),
                ("comment", models.TextField(blank=True, null=True)),
                ("last_updated", models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                ("min_members", models.PositiveIntegerField(default=1)),
                ("max_members", models.PositiveIntegerField(default=1)),
                ("is_registration_on", models.BooleanField(default=True)),
                ("slug", models.SlugField(default="default")),
            ],
        ),
        migrations.CreateModel(
            name="EventDetail",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                ("content", models.TextField()),
                ("priority", models.IntegerField()),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="website.Event"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Handles",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("codeforces", models.CharField(blank=True, max_length=100, null=True)),
                ("codechef", models.CharField(blank=True, max_length=100, null=True)),
                ("hackerrank", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "hackerearth",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "analyticsvidya",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("topcoder", models.CharField(blank=True, max_length=100, null=True)),
                ("dev_folio", models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                "verbose_name_plural": "Handles",
            },
        ),
        migrations.CreateModel(
            name="Membership",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=128, null=True)),
                (
                    "referral_code",
                    models.CharField(
                        default=website.models.generate_referral_code,
                        max_length=50,
                        unique=True,
                    ),
                ),
                (
                    "institute_type",
                    models.IntegerField(
                        choices=[(0, "School"), (1, "College"), (2, "Professional")],
                        null=True,
                    ),
                ),
                ("institute_name", models.CharField(default="", max_length=128)),
                ("study_year", models.PositiveIntegerField(null=True)),
                ("degree", models.CharField(blank=True, default="", max_length=50)),
                ("branch", models.CharField(blank=True, default="", max_length=100)),
                ("country", models.CharField(default="IN", max_length=4)),
                ("phone", models.CharField(blank=True, default="", max_length=15)),
                (
                    "gender",
                    models.IntegerField(
                        choices=[
                            (0, "Male"),
                            (1, "Female"),
                            (2, "Others/Not Specified"),
                        ],
                        null=True,
                    ),
                ),
                (
                    "resume",
                    models.FileField(
                        null=True, upload_to=website.models.Profile.get_file_path
                    ),
                ),
                ("is_profile_complete", models.BooleanField(default=False)),
                ("referral_count", models.IntegerField(default=0)),
                ("fcm_token", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "referred_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="referred",
                        to="website.Profile",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("is_active", models.BooleanField(default=False)),
                (
                    "access_code",
                    models.CharField(
                        default="uninitialized", max_length=100, unique=True
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="teams_created",
                        to="website.Profile",
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="website.Event"
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(
                        related_name="team_members",
                        through="website.Membership",
                        to="website.Profile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ValidReferral",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="referred_people",
                        to="website.Profile",
                    ),
                ),
                (
                    "to",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="referral",
                        to="website.Profile",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="membership",
            name="profile",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="website.Profile"
            ),
        ),
        migrations.AddField(
            model_name="membership",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="website.Team"
            ),
        ),
        migrations.AddField(
            model_name="handles",
            name="profile",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="handles",
                to="website.Profile",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="validreferral",
            unique_together={("by", "to")},
        ),
        migrations.AlterUniqueTogether(
            name="membership",
            unique_together={("team", "profile")},
        ),
    ]
