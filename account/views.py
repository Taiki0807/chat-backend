from django.middleware.csrf import get_token
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from rest_framework import status, response, permissions,generics,authentication
from rest_framework.views import APIView
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt import exceptions as jwt_exp
from rest_framework.validators import ValidationError
from rest_framework.response import Response
from .models import Account
from .serializers import AccountSerializer

class TokenObtainView(jwt_views.TokenObtainPairView):
    """
    JWTをCookieにセットして送る
    """

    def post(self, request, *args, **kwargs):
        # シリアライザーでバリデーションを行う．
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except jwt_exp.TokenError as e:
            raise jwt_exp.InvalidToken(e.args[0])

        # レスポンスオブジェクトの作成
        res = response.Response(data={
            'success': 1,
        },
            status=status.HTTP_200_OK
        )

        # Cookieの設定
        res.set_cookie(
            key="access_token",
            value=serializer.validated_data["access"],
            # max_age=60 * 60 * 24,
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            httponly=True,
        )
        res.set_cookie(
            key="refresh_token",
            value=serializer.validated_data["refresh"],
            # max_age=60 * 60 * 24 * 30,
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            httponly=True,
        )

        # csrftokenを設定
        get_token(request)
        return res

def refresh_get(request):
    """
    リフレッシュトークンを返す
    """
    try:
        rt = request.COOKIES["refresh_token"]
        return JsonResponse({"refresh": rt}, safe=False)
    except Exception as e:
        print(e)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

class TokenRefreshView(jwt_views.TokenRefreshView):
    """
    リフレッシュトークンを使って新しいアクセストークンを作成する
    """

    def post(self, request, *args, **kwargs):
        # シリアライザーによるバリデーション
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except jwt_exp.TokenError as e:
            raise jwt_exp.InvalidToken(e.args[0])

        # レスポンスオブジェクトの作成
        res = response.Response(status=status.HTTP_200_OK)
        res.set_cookie(
            key="access_token",
            value=serializer.validated_data["access"],
            # max_age=60 * 24 * 24 * 30,
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            httponly=True,
        )
        return res
class TokenDeleteView(APIView):
    """
    Cookieに保存しているTokenを削除する
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        res = response.Response(status=status.HTTP_200_OK)
        res.delete_cookie("access_token")
        res.delete_cookie("refresh_token")
        return res
class AccountRegister(generics.CreateAPIView):
    """
    アカウント登録を行う
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def perform_create(self, serializer):
        queryset = Account.objects.filter(username=self.request.data['username'])
        if queryset.exists():
            raise ValidationError('This username has already used')
        serializer.save()

class GetAccountInfo(APIView):
    """
    アカウント情報を取得する
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(data={
            'username': request.user.username,
        },
            status=status.HTTP_200_OK
        )
class GetAccountStatus(APIView):
    """
    状態を取得
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    def get(self, request):
        if request.COOKIES.get('access_token'):
            # cookieが存在する場合
            return Response({
                'status': 1,
            }, status=status.HTTP_200_OK)
        else:
            # cookieが存在しない場合
            return Response({
                'status': 0,
            }, status=status.HTTP_200_OK)