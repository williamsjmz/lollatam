import requests

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from lollatam.secrets import RIOT_API_KEY


@login_required
@require_http_methods(['GET'])
def get_summoner_stats(request, server, summoner):
    
    url = f'https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={RIOT_API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        
        account_data = response.json()
        account_id = account_data['id']

        url = f'https://{server}.api.riotgames.com/lol/league/v4/entries/by-summoner/{account_id}?api_key={RIOT_API_KEY}'
        response = requests.get(url)

        if response.status_code == 200:
            account_stats = response.json()
            return JsonResponse(account_stats, safe=False)
        
    return JsonResponse({'message': 'No statistics found for the account.'})
