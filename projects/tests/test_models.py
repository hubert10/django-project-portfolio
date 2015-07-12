from django.test import TestCase

from ..models import Project, Version


class ProjectManagerTests(TestCase):
    fixtures = ['projects.json']

    def test_live_projects(self):
        self.assertEqual(
            4, Project.objects.count()
        )

        self.assertEqual(
            2, Project.objects.live().count()
        )

        self.assertEqual(
            2, Project.objects.all().live().count()
        )

        self.assertEqual(
            ['Test Project 1', 'Test Project 2'],
            [p.name for p in Project.objects.live()]
        )


class VersionManagerTests(TestCase):
    fixtures = ['projects.json']

    def test_stable_query(self):
        queryset = Version.objects.all()
        self.assertEqual(
            2, queryset.stable().count()
        )

    def test_latest_toggle(self):
        versions = Project.objects.get(
            slug='test-project-1'
        ).versions

        self.assertEqual(
            1, versions.filter(
                is_latest=True
            ).count())

        for version in versions.all():
            latest = versions.filter(is_latest=True)
            if not version.is_latest:
                self.assertEqual(1, latest.count())
                self.assertFalse(version.id == latest[0].id)

            version.is_latest = True
            version.save()
            latest = versions.filter(is_latest=True)

            self.assertEqual(1, latest.count())
            self.assertEqual(version.id, latest[0].id)
            self.assertEqual(
                version.id,
                Project.objects.get(
                    pk=version.project.id
                ).latest_version().id)