from unittest.mock import AsyncMock, patch

from byuhbll.person_client.models import PersonSummary
from django.contrib.auth import get_user_model
from django.test import TestCase

from byuhbll_django_dry.signals import get_person_from_university, update_user_info

from .mock_data import TEST_PERSON_SUMMARY

GET_LIBRARY_ID = 'byuhbll.person_client.core.PersonClient.get_library_id'
GET_SUMMARY = 'byuhbll.person_client.core.PersonClient.get_summary'

User = get_user_model()


class SignalTests(TestCase):
    def setUp(self):
        self.library_id = TEST_PERSON_SUMMARY['library_id']
        self.user, _ = User.objects.get_or_create(username='somenetid')
        self.person_summary = PersonSummary(**TEST_PERSON_SUMMARY)
        self.user.library_id = self.library_id

    def tearDown(self):
        User.objects.all().delete()

    @patch(GET_SUMMARY, new_callable=AsyncMock)
    @patch(GET_LIBRARY_ID, new_callable=AsyncMock)
    def test_get_person_from_university(self, mock_library_id, mock_summary):
        mock_library_id.return_value = self.library_id
        mock_summary.return_value = self.person_summary

        person_summary = get_person_from_university(self.user.username)

        self.assertEqual(person_summary.library_id, self.library_id)

        mock_library_id.assert_called_once()
        mock_summary.assert_called_once()

    @patch(GET_SUMMARY, new_callable=AsyncMock)
    @patch(GET_LIBRARY_ID, new_callable=AsyncMock)
    def test_get_person_from_university_with_library_id(
        self, mock_library_id, mock_summary
    ):
        mock_library_id.return_value = self.library_id
        mock_summary.return_value = self.person_summary

        person_summary = get_person_from_university(
            self.user.username, library_id=self.library_id
        )

        self.assertEqual(person_summary.library_id, self.library_id)

        mock_library_id.assert_not_called()
        mock_summary.assert_called_once()

    @patch(GET_SUMMARY, new_callable=AsyncMock)
    @patch(GET_LIBRARY_ID, new_callable=AsyncMock)
    def test_update_user_info(self, mock_library_id, mock_summary):
        mock_library_id.return_value = self.library_id
        mock_summary.return_value = self.person_summary

        updated_user = update_user_info(self.user)

        self.assertEqual(updated_user.library_id, self.library_id)

        mock_library_id.assert_not_called()
        mock_summary.assert_called_once()

        self.assertEqual(
            updated_user.first_name, self.person_summary.preferred_first_name
        )
        self.assertEqual(updated_user.last_name, self.person_summary.last_name)
        self.assertEqual(updated_user.email, self.person_summary.email_address)

        self.user.refresh_from_db()

        self.assertEqual(self.user.first_name, self.person_summary.preferred_first_name)
        self.assertEqual(self.user.last_name, self.person_summary.last_name)
        self.assertEqual(self.user.email, self.person_summary.email_address)

    @patch(GET_SUMMARY, new_callable=AsyncMock)
    @patch(GET_LIBRARY_ID, new_callable=AsyncMock)
    def test_update_user_info_no_save(self, mock_library_id, mock_summary):
        mock_library_id.return_value = self.library_id
        mock_summary.return_value = self.person_summary

        updated_user = update_user_info(self.user, save=False)

        self.assertEqual(updated_user.library_id, self.library_id)

        mock_library_id.assert_not_called()
        mock_summary.assert_called_once()

        self.assertEqual(
            updated_user.first_name, self.person_summary.preferred_first_name
        )
        self.assertEqual(updated_user.last_name, self.person_summary.last_name)
        self.assertEqual(updated_user.email, self.person_summary.email_address)

        self.user.refresh_from_db()

        self.assertNotEqual(
            self.user.first_name, self.person_summary.preferred_first_name
        )
        self.assertNotEqual(self.user.last_name, self.person_summary.last_name)
        self.assertNotEqual(self.user.email, self.person_summary.email_address)
