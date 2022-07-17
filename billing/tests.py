from django.test import TestCase

# Create your tests here.

from django.test import TestCase, Client
from billing.passkey import encrypt, decrypt
class EncryptionTestCase(TestCase):
	def test_encrypt_decrypt(self):
		to_encrypt = 'Some text here'
		self.failUnlessEqual(to_encrypt, decrypt(encrypt(to_encrypt)))
		self.failIfEqual(to_encrypt, encrypt(to_encrypt))