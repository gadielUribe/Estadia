from django.test import TestCase, Client
from django.urls import reverse


class HerramientasViewsTests(TestCase):
    def test_list_requires_login(self):
        c = Client()
        resp = c.get(reverse("herramientas:herramienta_list"))
        # Redirige a login si no autenticado
        self.assertEqual(resp.status_code, 302)
