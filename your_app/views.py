from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from openai import OpenAI
from django.conf import settings

class ChatbotAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_message = request.data.get('message', '')
        if not user_message:
            return Response({'error': 'No message provided.'}, status=400)
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        system_prompt = "You are FoundrFuse AI, a helpful assistant for founders and investors. Answer clearly and concisely."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        bot_reply = response.choices[0].message.content
        return Response({'reply': bot_reply})