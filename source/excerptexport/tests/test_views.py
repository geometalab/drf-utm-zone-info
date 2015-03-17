from django.test import TestCase

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class ExcerptExportViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com', 'pw')
        self.new_excerpt_post_data = {
            'form-mode': 'create_new_excerpt',
            'new_excerpt.name': 'A very interesting region',
            'new_excerpt.is_public': 'True',
            'new_excerpt.boundingBox.north': '1.0',
            'new_excerpt.boundingBox.east': '2.0',
            'new_excerpt.boundingBox.south': '3.0',
            'new_excerpt.boundingBox.west': '4.0'
        }
        self.existing_excerpt_post_data = {
            'form-mode': 'existing_excerpt',
            'existing_excerpt.id': 'some_id'
        }

    def test_new_when_not_logged_in(self):
        """
        When not logged in, we get redirected.
        """
        response = self.client.get(reverse('excerptexport:new'))
        self.assertEqual(response.status_code, 302)

    def test_new(self):
        """
        When logged in, we get the excerpt choice form.
        """
        self.client.login(username='user', password='pw')
        response = self.client.get(reverse('excerptexport:new'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create new excerpt')

    def test_create_when_not_logged_in(self):
        """
        When not logged in, we get redirected.
        """
        response = self.client.post(reverse('excerptexport:create'), self.new_excerpt_post_data)
        self.assertEqual(response.status_code, 302)

    def test_create_with_new_excerpt(self):
        """
        When logged in, POSTing an export request with a new excerpt is successful.
        """
        self.client.login(username='user', password='pw')
        response = self.client.post(reverse('excerptexport:create'), self.new_excerpt_post_data)
        self.assertEqual(response.status_code, 200)

    def test_create_with_existing_excerpt(self):
        """
        When logged in, POSTing an export request using an existing excerpt is successful.
        """
        self.client.login(username='user', password='pw')
        response = self.client.post(reverse('excerptexport:create'), self.existing_excerpt_post_data)
        self.assertEqual(response.status_code, 200)
