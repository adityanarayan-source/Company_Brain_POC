from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent import run_agent
from database import init_db, save_log
from models import ChatRequest

app = FastAPI(title='Mini Company Brain API')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173'], allow_methods=['*'], allow_headers=['*'])
init_db()


@app.get('/')
def root(): return {'message': 'Mini Company Brain API is running'}


@app.get('/health')
def health(): return {'status': 'ok'}


@app.post('/chat')
def chat(request: ChatRequest):
    response, activity = run_agent(request.user_id, request.message)
    save_log(request.user_id, request.message, activity['tool'], activity['status'])
    return {'response': response, 'activity': activity}
