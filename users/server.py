import logging
import json

from aiohttp import web

import core

from users import (errors, state, types)
from users.db import users

LOGGER = logging.getLogger(__name__)

class Server:
    """Contains HTTP route methods for the Users Service API."""

    def __init__(self, state: state.State):
        self._encoder = types.ResponseEncoder()
        self._state = state
    

    async def health(self, request):
        return web.json_response({"name": "user-service"}, status=200)
    
    
    async def get_user(self, request):
        try:
            u = self._state.users_repo.lookup(request.match_info["user_id"])
        except Exception as e:
            return self._write_error(e)

        res = self._encoder.encode(u)

        return web.Response(
            body=res,
            status=200,
            content_type="application/json"
        )


    async def get_users(self, request):
        try:
            users = self._state.users_repo.list_all()
        except Exception as e:
            return self._write_error(e)

        res = self._encoder.encode(users)

        return web.Response(
            body=res,
            status=200,
            content_type="application/json"
        )


    async def create_user(self, request):
        body = await request.json()
        try:
            uid = self._state.users_repo.create(body["name"],
                body["email"])

            u = self._state.users_repo.lookup(uid)
        except Exception as e:
            return self._write_error(e)        

        res = self._encoder.encode(u)
        
        return web.Response(
            body=res,
            status=200,
            content_type="application/json"
        )


    async def update_user(self, request):
        body = await request.json()
        try:
            self._state.users_repo.update_details(
                request.match_info["user_id"], body["name"], body["email"])

            user = self._state.users_repo.lookup(request.match_info["user_id"])
        except Exception as e:
            return self._write_error(e)
        
        res = self._encoder.encode(user)

        return web.Response(
            body=res,
            status=200,
            content_type="application/json"
        )


    async def delete_user(self, request):
        try:
            self._state.users_repo.delete(request.match_info["user_id"])
        except Exception as e:
            return self._write_error(e)

        return web.json_response({}, status=204)
    
    def _write_error(self, e: Exception):
        LOGGER.error(e)
        return web.json_response(
            {"error": str(e)},
            status=errors.status_code(e),
        )


def init(state: state.State):
    server = Server(state)

    app = web.Application()
    app.add_routes([
        web.get("/", server.health),

        web.get("/users", server.get_users),
        web.post("/users", server.create_user),

        web.get("/users/{user_id}", server.get_user),
        web.put("/users/{user_id}", server.update_user),
        web.delete("/users/{user_id}", server.delete_user)
    ])

    return app
