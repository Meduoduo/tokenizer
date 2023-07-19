from flask import request
from routine.exchange import caculate_money
from utils.token import openai_num_tokens_from_messages, get_token_cost
import json

def token_cost():
    try:
        token = request.form['token']
        model = request.form['model']
        copyright = request.form['copyright']
        functions = request.form['functions']

        model = model.lower()

        try:
            message = json.loads(token)
            if type(message) is not list:
                message = [{
                    'role' : 'user',
                    'content' : message
                }]
            message += [{
                'role' : 'functions',
                'content' : functions
            }]
        except:
            message = token + functions

        if copyright == "OpenAI":
            num_tokens = openai_num_tokens_from_messages(message, model=model)
        else:
            num_tokens = 0
        
        usd = get_token_cost(model, num_tokens)
        cny = caculate_money(usd, 'USD', 'CNY')
        eur = caculate_money(usd, 'USD', 'EUR')
        jpy = caculate_money(usd, 'USD', 'JPY')

        result = {
            'token': num_tokens,
            'USD': usd,
            'CNY': cny,
            'EUR': eur,
            'JPY': jpy,
        }

        return json.dumps({
            'code': 0,
            'message': 'success',
            'copyright': 'Miduoduo',
            'result': result,
        })
    except Exception as e:
        return json.dumps({
            'code': 1,
            'message': "An unknown error occurred.",
            'copyright': 'Miduoduo',
            'result': {},
        })