import json
import re
from config import OPENAI_API_KEY
from memory import get_memories, save_memory
from tools import TOOLS


def choose_tool(message):
    lower = message.lower()
    if re.search(r'analy[sz]e|character count|word count', lower): return 'content_analyzer'
    if re.search(r'\b(calculate|what is)\b.*[0-9].*[+\-*/]', lower): return 'calculator'
    if any(word in lower for word in ('refund', 'support', 'company product')): return 'company_search'
    return None


def extract_preference(message):
    lower = message.lower()
    if any(trigger in lower for trigger in ('from now on', 'prefer', 'keep my content', 'no emojis')):
        return message.strip()
    return None


def run_agent(user_id, message):
    memories = get_memories(user_id, message)
    preference = extract_preference(message)
    if preference: save_memory(user_id, preference)
    tool_name = choose_tool(message)
    tool_result, status = 'No tool needed', 'success'
    if tool_name:
        try:
            raw_input = re.sub(r'^.*?(analy[sz]e|calculate|what is)\s*', '', message, flags=re.I).strip(' :')
            value = TOOLS[tool_name](raw_input or message)
            tool_result = json.dumps(value) if isinstance(value, dict) else value
            if isinstance(value, dict) and value.get('valid') is False: status = 'error'
        except Exception as error:
            tool_result, status = str(error), 'error'
    response = build_response(message, memories, tool_name, tool_result)
    return response, {'memories': memories, 'tool': tool_name, 'tool_result': tool_result, 'status': status}


def build_response(message, memories, tool_name, tool_result):
    if tool_name == 'content_analyzer': return f'Content analysis: {tool_result}'
    if tool_name == 'calculator': return f'The answer is {tool_result}.'
    if tool_name == 'company_search': return tool_result
    if extract_preference(message): return 'Understood. I saved that preference and will apply it in future conversations.'
    if OPENAI_API_KEY:
        try:
            from openai import OpenAI
            context = '; '.join(memories) or 'No saved preferences.'
            prompt = f'User preferences: {context}\nUser request: {message}\nAnswer concisely and follow the preferences.'
            return OpenAI(api_key=OPENAI_API_KEY).responses.create(model='gpt-4o-mini', input=prompt).output_text
        except Exception:
            pass  # The deterministic demo response keeps the POC usable if the API is unavailable.
    options = ['A clear, customer-focused announcement.', 'A practical product benefit with a strong hook.', 'A short invitation to learn more.']
    memory_note = f' I will also follow your saved preferences: {"; ".join(memories)}.' if memories else ''
    return 'Here are three options:\n\n' + '\n'.join(f'{index}. {option}' for index, option in enumerate(options, 1)) + memory_note
