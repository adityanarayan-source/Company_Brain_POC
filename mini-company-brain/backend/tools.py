import re


def calculator(expression):
    # Demo calculator accepts only numbers and arithmetic operators.
    if not re.fullmatch(r'[0-9+\-*/(). %]+', expression):
        raise ValueError('Only basic arithmetic is supported')
    return str(eval(expression, {'__builtins__': {}}, {}))


def company_search(query):
    knowledge = {'product': 'Our AI workspace helps teams find knowledge and create content.', 'refund': 'Refund requests are reviewed by support within 5 business days.', 'support': 'Contact support@example.com for help.'}
    return next((value for key, value in knowledge.items() if key in query.lower()), 'No matching company information found.')


def content_analyzer(text):
    characters = len(text)
    result = {'characters': characters, 'words': len(text.split()), 'valid': characters <= 200}
    if not result['valid']:
        result['reason'] = 'Content exceeds 200 characters'
    return result


TOOLS = {'calculator': calculator, 'company_search': company_search, 'content_analyzer': content_analyzer}
