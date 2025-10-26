from django.test import TestCase
from django.urls import reverse


class ProvasFlowTest(TestCase):
    def setUp(self):
        # Registrar e autenticar usuário
        self.register_url = reverse("register")
        self.token_url = reverse("token_obtain_pair")
        self.profile_url = reverse("profile")

        r = self.client.post(
            self.register_url,
            {
                "username": "u1",
                "email": "u1@example.com",
                "password": "SenhaForte123",
                "first_name": "U",
                "last_name": "One",
            },
            content_type="application/json",
        )
        assert r.status_code in (200, 201, 204), r.content

        r = self.client.post(
            self.token_url,
            {"email": "u1@example.com", "password": "SenhaForte123"},
            content_type="application/json",
        )
        assert r.status_code == 200, r.content
        self.access = r.json()["access"]
        self.auth = {"HTTP_AUTHORIZATION": f"Bearer {self.access}"}

    def test_crud_and_summary_and_jobs(self):
        # Create Prova
        list_url = reverse("provas-list")
        r = self.client.post(
            list_url,
            {"titulo": "Simulado 1", "descricao": "Teste", "questoes": 10},
            content_type="application/json",
            **self.auth,
        )
        self.assertEqual(r.status_code, 201, r.content)
        prova_id = r.json()["id"]

        # List
        r = self.client.get(list_url, **self.auth)
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(len(r.json()), 1)

        # Summary action
        summary_url = reverse("provas-summary")
        r = self.client.get(summary_url, **self.auth)
        self.assertEqual(r.status_code, 200)
        self.assertIn("total", r.json())

        # Gerar job
        gerar_url = reverse("provas-gerar")
        r = self.client.post(
            gerar_url,
            {"texto": "Matemática básica", "questoes": 5},
            content_type="application/json",
            **self.auth,
        )
        self.assertEqual(r.status_code, 201, r.content)
        job_id = r.json()["id"]

        # Retrieve job
        from django.urls import NoReverseMatch

        try:
            job_detail_url = reverse("jobs-detail", kwargs={"pk": job_id})
        except NoReverseMatch:
            # Fallback in case basename differs
            job_detail_url = f"/api/provas/jobs/{job_id}/"

        r = self.client.get(job_detail_url, **self.auth)
        self.assertEqual(r.status_code, 200, r.content)

        # Cancel job
        try:
            cancelar_url = reverse("jobs-cancelar", kwargs={"pk": job_id})
        except NoReverseMatch:
            cancelar_url = f"/api/provas/jobs/{job_id}/cancelar/"
        r = self.client.post(cancelar_url, **self.auth)
        self.assertEqual(r.status_code, 200, r.content)

