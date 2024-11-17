from django.test import TestCase
from django.core import mail
from django.urls import reverse
from users.models import User

class UserRegistrationTest(TestCase):
    def test_user_registration_sends_email(self):
        # 회원가입 데이터를 준비합니다.
        user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@example.com'
        }

        # 회원가입 요청을 보냅니다.
        response = self.client.post(reverse('user-list-create'), user_data)

        # 응답이 성공적인지 확인합니다.
        self.assertEqual(response.status_code, 201)

        # 이메일이 하나 전송되었는지 확인합니다.
        self.assertEqual(len(mail.outbox), 1)

        # 전송된 이메일의 내용을 확인합니다.
        sent_email = mail.outbox[0]
        self.assertEqual(sent_email.subject, 'Verify your email')
        self.assertIn('Click the link to verify your email', sent_email.body)
        self.assertEqual(sent_email.to, [user_data['email']])