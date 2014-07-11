# -*- coding: utf-8 -*-

from urlparse import urlparse

from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse
from django.test import SimpleTestCase

from ..forms import AddTicketForm
from ..models import Meeting
from ..views import MeetView

User = get_user_model()
HTTP_METHOD_NAMES = ['get', 'post', 'put', 'patch', 'delete']


class TestMeetView(SimpleTestCase):

    @classmethod
    def setUpClass(cls):
        cls.url = reverse('meet')
        cls.username = 'testuser'
        cls.password = 'password'
        try:
            cls.user = User.objects.get(username=cls.username)
        except User.DoesNotExist:
            cls.user = User.objects.create_user(cls.username, 'test@example.com', cls.password)
        cls.meeting = Meeting.objects.get_current_meeting(cls.user)

    @classmethod
    def tearDownClass(cls):
        Meeting.objects.all().delete()

    def tearDown(self):
        self.client.logout()

    def test_login_required_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(302, response.status_code)
        self.assertEqual('login', resolve(urlparse(response.url).path).url_name)

    def test_login_required_logged_in(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_allowed_methods(self):
        self.client.login(username=self.username, password=self.password)
        allowed_methods = ['get']
        for method in HTTP_METHOD_NAMES:
            request_method = getattr(self.client, method)
            response = request_method(self.url)
            expected_status_code = 200 if method in allowed_methods else 405
            self.assertEqual(expected_status_code, response.status_code)

    def test_get_context_data(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(self.meeting, response.context['meeting'])
        self.assertTrue(isinstance(response.context['form'], AddTicketForm))