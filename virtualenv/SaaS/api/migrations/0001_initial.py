# Generated by Django 2.1.3 on 2018-12-04 22:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Curator',
            fields=[
                ('name', models.CharField(max_length=35)),
                ('last_name', models.CharField(max_length=35)),
                ('patronymic', models.CharField(max_length=35)),
                ('description', models.CharField(max_length=200)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('credentials', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Curator',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Skill',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('name', models.CharField(max_length=35)),
                ('last_name', models.CharField(max_length=35)),
                ('patronymic', models.CharField(max_length=35)),
                ('description', models.CharField(max_length=200)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('credentials', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('skills', models.ManyToManyField(to='api.Skill')),
            ],
            options={
                'db_table': 'Student',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Subject',
            },
        ),
        migrations.CreateModel(
            name='SuggestionTheme',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_creation', models.DateTimeField()),
                ('curator', models.ForeignKey(db_column='curator_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Curator')),
            ],
            options={
                'db_table': 'Suggestion_theme',
            },
        ),
        migrations.CreateModel(
            name='SuggestionThemeComment',
            fields=[
                ('author_name', models.CharField(max_length=35)),
                ('content', models.CharField(max_length=200)),
                ('date_creation', models.DateTimeField()),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('suggestion', models.ForeignKey(db_column='suggestion_id', on_delete=django.db.models.deletion.CASCADE, related_name='comment_set', to='api.SuggestionTheme')),
            ],
            options={
                'db_table': 'Suggestion_theme_comment',
            },
        ),
        migrations.CreateModel(
            name='SuggestionThemeProgress',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=75)),
                ('description', models.CharField(max_length=150)),
                ('date_update', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'Suggestion_theme_progress',
            },
        ),
        migrations.CreateModel(
            name='SuggestionThemeStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Suggestion_theme_status',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=250)),
                ('date_creation', models.DateTimeField()),
                ('date_acceptance', models.DateTimeField(null=True)),
                ('curator', models.ForeignKey(db_column='curator_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Curator')),
                ('skills', models.ManyToManyField(to='api.Skill')),
                ('student', models.ForeignKey(db_column='student_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Student')),
                ('subject', models.ForeignKey(db_column='subject_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Subject')),
            ],
            options={
                'db_table': 'Theme',
            },
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_start', models.DateTimeField()),
                ('date_finish', models.DateTimeField(null=True)),
                ('theme', models.ForeignKey(db_column='theme_id', on_delete=django.db.models.deletion.CASCADE, to='api.Theme')),
            ],
            options={
                'db_table': 'Work',
            },
        ),
        migrations.CreateModel(
            name='WorkStep',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=250)),
                ('date_start', models.DateTimeField()),
                ('date_finish', models.DateTimeField()),
            ],
            options={
                'db_table': 'Work_step',
            },
        ),
        migrations.CreateModel(
            name='WorkStepComment',
            fields=[
                ('author_name', models.CharField(max_length=35)),
                ('content', models.CharField(max_length=200)),
                ('date_creation', models.DateTimeField()),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('step', models.ForeignKey(db_column='work_step_id', on_delete=django.db.models.deletion.CASCADE, related_name='comment_set', to='api.WorkStep')),
            ],
            options={
                'db_table': 'Work_step_comment',
            },
        ),
        migrations.CreateModel(
            name='WorkStepMaterial',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=200)),
                ('step', models.ForeignKey(db_column='step_id', on_delete=django.db.models.deletion.CASCADE, related_name='material_set', to='api.WorkStep')),
            ],
            options={
                'db_table': 'Work_step_material',
            },
        ),
        migrations.CreateModel(
            name='WorkStepStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Work_step_status',
            },
        ),
        migrations.AddField(
            model_name='workstep',
            name='status',
            field=models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.DO_NOTHING, to='api.WorkStepStatus'),
        ),
        migrations.AddField(
            model_name='workstep',
            name='work',
            field=models.ForeignKey(db_column='work_id', on_delete=django.db.models.deletion.CASCADE, related_name='step_set', to='api.Work'),
        ),
        migrations.AddField(
            model_name='suggestiontheme',
            name='progress',
            field=models.ForeignKey(db_column='progress_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.SuggestionThemeProgress'),
        ),
        migrations.AddField(
            model_name='suggestiontheme',
            name='status',
            field=models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.DO_NOTHING, to='api.SuggestionThemeStatus'),
        ),
        migrations.AddField(
            model_name='suggestiontheme',
            name='student',
            field=models.ForeignKey(db_column='student_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Student'),
        ),
        migrations.AddField(
            model_name='suggestiontheme',
            name='theme',
            field=models.ForeignKey(db_column='theme_id', on_delete=django.db.models.deletion.CASCADE, to='api.Theme'),
        ),
        migrations.AddField(
            model_name='curator',
            name='skills',
            field=models.ManyToManyField(to='api.Skill'),
        ),
    ]
