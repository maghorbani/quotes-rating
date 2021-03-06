from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Quote, Rate
from django.contrib.auth.models import User

import random


class BasicTest(TestCase):
    def setUp(self):
        u1 = User.objects.create_user('john', 'lennon@test.com', 'johnpassword')
        u2 = User.objects.create_user('doe', 'doe@test.com', 'doepassword')
        Quote.objects.create(title="A", body="AAA", user=u1)
        Quote.objects.create(title="B", body="BBB", user=u1)
        client = APIClient()
        res = client.post("/api/auth/login/", {
            "username": "john",
            "password": "johnpassword"
        })
        self.token = res.data['access']
        res = client.post("/api/auth/login/", {
            "username": "doe",
            "password": "doepassword"
        })
        self.token2 = res.data['access']

    def test_view_quotes(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT " + self.token)
        res = client.get(reverse('quote'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)

    def test_add_quote(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT " + self.token)
        res = client.post(reverse('quote'), {"title": "C", "body": "CCC"})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['title'], "C")

    def test_rate(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT " + self.token)
        res = client.post(reverse("rate_a_quote", kwargs={'pk': 1}), {"score": 4})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['score'], 4)

        res = client.post(reverse("rate_a_quote", kwargs={'pk': 2}), {"score": 3})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['score'], 3)

        # changing to user doe
        client.credentials(HTTP_AUTHORIZATION="JWT " + self.token2)

        res = client.post(reverse("rate_a_quote", kwargs={'pk': 1}), {"score": 3})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['score'], 3)

        res = client.post(reverse("rate_a_quote", kwargs={'pk': 2}), {"score": 5})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['score'], 5)

        res = client.get(reverse('get_quote', kwargs={"pk": 1}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["average_score"], 3.5)
        self.assertEqual(res.data["your_score"], 3)

        res = client.get(reverse('get_quote', kwargs={"pk": 2}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["average_score"], 4)
        self.assertEqual(res.data["your_score"], 5)

        client.credentials(HTTP_AUTHORIZATION="JWT " + self.token)

        # changin score to see if the average score changes
        res = client.post(reverse("rate_a_quote", kwargs={'pk': 2}), {"score": 4})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['score'], 4)

        res = client.get(reverse('get_quote', kwargs={"pk": 2}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["average_score"], 4.5)
        self.assertEqual(res.data["your_score"], 4)


class LargeNumberOfUsersTest(TestCase):
    def setUp(self):
        u1 = User.objects.create_user('john', 'lennon@test.com', 'johnpassword')
        Quote.objects.create(title="A", body="AAA", user=u1)

        client = APIClient()
        res = client.post("/api/auth/login/", {
            "username": "john",
            "password": "johnpassword"
        })
        self.token = res.data['access']

        self.rates = [random.randint(0, 5) for i in range(500)]
        for i in range(500):
            u1 = User.objects.create_user('user{}'.format(i), 'user{}@test.com'.format(i), '123456')
            res = client.post("/api/auth/login/", {
                "username": "user{}".format(i),
                "password": "123456"
            })
            token = res.data['access']

            client.credentials(HTTP_AUTHORIZATION="JWT " + token)
            res = client.post(reverse("rate_a_quote", kwargs={'pk': 1}), {"score": self.rates[i]})

        self.avg = 0
        for s in self.rates:
            self.avg += s
        self.avg /= 500

    def test_average(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT " + self.token)
        res = client.get(reverse('get_quote', kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 200)
        self.assertAlmostEqual(res.data['average_score'], self.avg, delta=1e4)
