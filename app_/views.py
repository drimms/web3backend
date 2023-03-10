from web3 import Web3
import requests, json
from .models import Lead
from .serialize import LeadSerializer
from rest_framework import generics
import threading
from django.conf import settings
from django.http import HttpResponse

apikey = 'BQ28PYWIEQZDQWTUP5ZHPY7TMKS97MVGWE'
token = "0x09757dabac779e8420b40df0315962bbc9833c73"
link = f'https://api-goerli.etherscan.io/api?module=account&action=txlist&address={token}&startblock=0&endblock=99999999&sort=asc&apikey={apikey}'
tr = Web3.keccak(text='approve(address spender, uint256 tokens)') #за это могу объяснить


class LeadListCreate(generics.ListAPIView):
    serializer_class = LeadSerializer
    queryset = Lead.objects.all()

    def get_queryset(self):
        get_query()
        queryset = Lead.objects.all()
        timer = threading.Timer(settings.EXTERNAL_DATA_UPDATE_INTERVAL, get_query)
        timer.daemon = True
        timer.start()
        return queryset

def get_query():

    web3 = Web3(Web3.HTTPProvider('https://goerli.etherscan.io'))
    response = requests.get(link)
    tx_list = response.json()['result']
    last_100_records = tx_list[-100:]
    Lead.objects.all().delete()  # возможно не надо удалять старые записи?
    for tx in last_100_records:
        tx_hash = tx['hash']
        gas_used = int(tx['gasUsed'])
        stat = web3.fromWei((gas_used * int(tx['gasPrice'])), 'ether')
        action = tx['functionName']

        if web3.keccak(text=action) == tr:
            action = 'Approve'
        else:
            action = 'Transfer'

        b = Lead(hashname=tx_hash,
                 typeaction=action,
                 summ=stat.normalize())
        b.save()

