from typing import Any

from flask import url_for

from tests.base import TestBaseCase


class MailTests(TestBaseCase):

    def test_mail(self) -> None:
        rv: Any = self.app.post(
            url_for('newsletter'),
            data={'subject': 'test', 'body': 'test', 'recipient': []},
            follow_redirects=True)
        assert b'Newsletter send: 0' in rv.data

        rv = self.app.post(
            url_for('settings', category='mail'),
            data={
                'mail': True,
                'mail_transport_username': 'whatever',
                'mail_transport_host': 'localhost',
                'mail_transport_port': '23',
                'mail_from_email': 'max@example.com',
                'mail_from_name': 'Max Headroom',
                'mail_recipients_feedback': 'headroom@example.com'},
            follow_redirects=True)
        assert b'Max Headroom' in rv.data

        rv = self.app.get(url_for('index_unsubscribe', code='666'))
        assert b'invalid' in rv.data

        rv = self.app.get(url_for('index_unsubscribe', code='1234'))
        assert b'You have successfully unsubscribed' in rv.data

        rv = self.app.post(
            url_for('admin_index'),
            data={'receiver': 'test@example.com'},
            follow_redirects=True)
        assert b'A test mail was sent' in rv.data

        rv = self.app.get(url_for('newsletter'))
        assert b'Newsletter' in rv.data

        rv = self.app.post(
            url_for('newsletter'),
            data={
                'subject': 'test',
                'body': 'test',
                'recipient': [self.alice_id]},
            follow_redirects=True)
        assert b'Newsletter send: 1' in rv.data

        rv = self.app.get(url_for('index_feedback'))
        assert b'Thank you' in rv.data

        rv = self.app.post(
            url_for('index_feedback'),
            data={'subject': 'question', 'description': 'Why me?'},
            follow_redirects=True)
        assert b'Thank you for your feedback' in rv.data

        rv = self.app.post(
            url_for('user_insert'),
            data={
                'active': '',
                'username': 'Ripley',
                'email': 'ripley@nostromo.org',
                'password': 'you_never_guess_this',
                'password2': 'you_never_guess_this',
                'group': 'admin',
                'name': 'Ripley Weaver',
                'real_name': '',
                'description': '',
                'send_info': True},
            follow_redirects=True)
        assert b'A user was created' in rv.data

        rv = self.app.get(url_for('reset_password'))
        assert b'Forgot your password?' not in rv.data

        self.app.get(url_for('logout'))
        rv = self.app.get(url_for('reset_confirm', code='6666'))
        assert b'Invalid' in rv.data

        rv = self.app.get(
            url_for('reset_confirm', code='1234'),
            follow_redirects=True)
        assert b'A new password was sent to' in rv.data

        rv = self.app.get(url_for('reset_confirm', code='5678'))
        assert b'expired' in rv.data

        rv = self.app.post(
            url_for('reset_password'),
            data={'email': 'alice@example.com'},
            follow_redirects=True)
        assert b'password reset confirmation mail was send' in rv.data

        rv = self.app.post(
            url_for('reset_password'),
            data={'email': 'non-exising@example.com'})
        assert b'this email address is unknown to us' in rv.data
