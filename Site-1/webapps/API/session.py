from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.sessions.backends.db import SessionStore

from django.contrib.auth import authenticate

class SessionView(APIView):
    def post(self, request, format=None):
        try:
            username= request.data['username']
            password= request.data['password']
            user = authenticate(username=username, password=password)
            if user:
                session= SessionStore()
                session['user_id']=user.id
                session.create()
                return Response({'session_key': session.session_key, 'username': user.first_name}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error_msg': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error_msg': 'error'}, status=status.HTTP_400_BAD_REQUEST)

class SessionDetailView(APIView):
    def delete(self, request, session_key):
        try:
            session = SessionStore(session_key=session_key)
            session.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def get(self, request, session_key):
        session = SessionStore(session_key=session_key)
        return Response({'user_id' : session['user_id']})



