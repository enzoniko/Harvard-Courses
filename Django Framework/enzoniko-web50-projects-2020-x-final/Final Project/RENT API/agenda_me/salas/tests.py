from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Sala

# TESTAR CRIACAO DA SALA
class ModelSalaTestCase(TestCase):
    """Testando o model Sala."""
    def setUp(self):
        """Variaveis iniciais para o teste."""
        """Por padrão vou usar nomes de ruas."""
        self.name = "Rua Augusta"
        self.sala = Sala(name=self.name)

    def test_model_can_create_a_sala(self):
        """Testando se foi inserido no banco"""
        count_anterior = Sala.objects.count()
        self.sala.save()
        count_atual = Sala.objects.count()
        self.assertNotEqual(count_anterior, count_atual)

    def test_model_sala_to_str(self):
        """Testando se o metodo __str__"""
        count_anterior = Sala.objects.count()
        self.sala.save()        
        self.assertEqual(str(self.sala), self.name)

# TESTAR END POINTS
class ViewTestCase(TestCase):  

    def setUp(self):
        """Variaveis iniciais para o teste."""
        self.client = APIClient()
        self.sala_data = {'name': 'Av Paulista'}
        self.response = self.client.post(
            reverse('create_sala'),
            self.sala_data,
            format="json")

    def test_api_can_create_a_sala(self):
        """Testando a criacao da sala via post"""                
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)        
    
    def test_api_can_get_a_sala(self):
        """Test the api can get a given sala."""
        sala = Sala.objects.get()       
        response = self.client.get(
            reverse('details_sala',
            kwargs={'pk': sala.id}), format="json")        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, sala) 
  
    def test_api_can_update_sala(self):        
        """Test the api can update a given sala."""
        sala = Sala.objects.get()   
        change_sala = {'name': 'Radial Leste'}
        res = self.client.put(
                reverse('details_sala', kwargs={'pk': sala.id}),
                change_sala, 
                headers=({'Content-Type':'application/json'}))        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_api_can_delete_sala(self):
        """Test the api can delete a sala."""
        sala = Sala.objects.get()
        res = self.client.delete(
            reverse('details_sala', kwargs={'pk': sala.id}),
            format='json',
            follow=True)        
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)