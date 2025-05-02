# [How to run]
# uvicorn main:app --reload
# curl -X POST  -H "Content-Type: application/json" 'http://127.0.0.1:8000/items?item=apple'
# curl -X GET  -H "Content-Type: application/json" http://127.0.0.1:8000/items/1
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import RedirectResponse

app = FastAPI()

class Item(BaseModel):
	text: str
	is_done: bool = False
	
items = []

@app.post("/items")
def create_item(item: Item):
	items.append(item)
	return items

@app.get("/items", response_model=list[Item])
def list_items(limit: int = 10):
    return items[0:limit]

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
	if item_id < len(items):
		return items[item_id]
	else:
		raise HTTPException(status_code=404, detail="Item not found")

# [Reference]
# https://docs.github.com/ko/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps
github_client_id = ''
github_client_secret = ''

@app.get("/github-login")
async def github_login():
	return RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={github_client_id}')

@app.get("/github-code")
async def github_code(code: str):
	params = {
		'client_id': github_client_id,
		'client_secret': github_client_secret,
		'code': code
    }
	headers = {
		'Accept': 'application/json'
    }
	async with httpx.AsyncClient() as client:
		response = await client.post(url='https://github.com/login/oauth/access_token', params=params, headers=headers)
	response_json = response.json()
	access_token = response_json['access_token']
	async with httpx.AsyncClient() as client:
		headers.update({'Authorization': f'Bearer {access_token}'})
		response = await client.get('https://api.github.com/user', headers=headers)
	return response.json()
