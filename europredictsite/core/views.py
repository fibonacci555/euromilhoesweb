from django.shortcuts import render
from django.views.generic import View
from .utils import predict
import json
from django.http import JsonResponse
import pandas as pd
from datetime import datetime
import os
# Create your views here.
class HomeView(View):
    def get(self, request):
        # Ler o último número do arquivo results.xlsx
        
        df = pd.read_excel('results.xlsx')
                
        # Verificar qual coluna contém a data
        # Substitua 'Date' pelo nome correto da coluna de data se for diferente

        ano_atual = str(datetime.now().year)

        # Filtrar as linhas que contêm o ano atual na coluna 'Date'
        linhas_filtradas = df[df['Date'].astype(str).str.contains(ano_atual)]
        linha = linhas_filtradas.iloc[0]
        
        context = {
            'last_numbers': f"{linha['Numero1']}, {linha['Numero2']}, {linha['Numero3']}, {linha['Numero4']}, {linha['Numero5']} | {linha['Estrela1']}, {linha['Estrela2']} - Data: {linha['Date']}",
        }
        return render(request, 'index.html', context)
    
    def post(self, request):
        print("Post feito")
        data = json.loads(request.body)
        print("Dados recebidos:")
        print(data)
        num_predictions = int(data.get('num_predictions', 1))
        predictions = [predict() for _ in range(num_predictions)]
        return JsonResponse({'predictions': predictions})