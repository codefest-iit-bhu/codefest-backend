from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import authentication, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .services.eval_expr import ExpressionEvaluator
import ast

from .models import *
from .serializers import *
from django.utils.timezone import now
import math


# Create your views here.
class UserInfoCreateView(generics.CreateAPIView):
    http_method_names = ["post"]
    serializer_class = UserInfoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer.validated_data


class UserInfoRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    lookup_field = "pk"

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        if pk:
            return UserInfo.objects.filter(id=pk)
        return UserInfo.objects.all()

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        if pk:
            return self.retrieve(request, *args, **kwargs)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        if self.get_queryset().first().user != self.request.user:
            raise PermissionDenied(
                detail="You are not allowed to update other users info"
            )
        serializer.save(user=self.request.user)
        return serializer.validated_data


class RoundInfoCreateView(generics.CreateAPIView):
    http_method_names = ["post"]
    serializer_class = RoundInfoSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    # def perform_create(self, serializer):
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return serializer.validated_data


class RoundInfoRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoundInfoSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    lookup_field = "round_number"

    def get_queryset(self):
        return RoundInfo.objects.filter(round_number=self.kwargs.get("round_number"))


class ErrorInfoCreateView(generics.CreateAPIView):
    http_method_names = ["post"]
    serializer_class = ErrorInfoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    def perform_create(self, serializer):
        round_number = self.request.data.get("round_number")
        round = RoundInfo.objects.filter(round_number=round_number)
        if not round.exists():
            raise ParseError(detail="Round does not exist")

        u_info = UserInfo.objects.filter(user=self.request.user)
        if not u_info.exists():
            raise ParseError(detail="User not registered for contest")
        serializer.is_valid(raise_exception=True)
        serializer.save(user_info=u_info.first(), round=round.first())
        return serializer.validated_data


class ErrorInfoRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ErrorInfoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    lookup_field = "round"

    def get_queryset(self):
        return ErrorInfo.objects.filter(
            round__round_number=self.kwargs.get("round"),
            user_info__user=self.request.user,
        )

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.validated_data


class RoundInfoPublicView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    def get_serializer_class(self):
        fields = None
        if not self.kwargs.get("round_id"):
            fields = ['id', 'round_number', 'start_time', 'end_time','training_points', 'problem_statement']

        return lambda *args, **kwargs: RoundInfoPublicSerializer(*args, fields=fields, **kwargs)

    def get_queryset(self, request, *args, **kwargs):
        round_id = self.kwargs.get("round_id")
        if round_id:
            round_info = get_object_or_404(RoundInfo, id=round_id)
            return round_info
        else:
            return RoundInfo.objects.all()

    def get(self, request, *args, **kwargs):
        round_info = self.get_queryset(request)
        serializer_class = self.get_serializer_class()

        serializer = serializer_class(round_info, many=not isinstance(round_info, RoundInfo))

        # if isinstance(round_info, RoundInfo) and round_info.start_time > now():
        #     raise PermissionDenied(
        #         detail=f"You can only view this round from {round_info.start_time}"
        #     )

        return Response(serializer.data)


class CalculateErrorView(generics.CreateAPIView):
    serializer_class = LatexExpressionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    def get_required_data(self, request):
            latex_expression = request.data.get('latex_expression')
            round_id = request.data.get('round_id')
            bidding_amount = request.data.get('bidding_amount')
            user_info = get_object_or_404(UserInfo, user=request.user)
            state = request.data.get('state')

            if not latex_expression or not round_id:
                raise ValueError("Missing data.")

            return latex_expression, round_id, user_info, state, bidding_amount

    def get_round_info(self, round_id, state):
        try:
            round_info = RoundInfo.objects.get(id=round_id)
            if state == 'test':
                points = ast.literal_eval(round_info.testing_points)
            else:
                points = ast.literal_eval(round_info.training_points)
            return round_info, points
        except RoundInfo.DoesNotExist:
            raise ValueError("Round not found.")
        except SyntaxError:
            raise ValueError("Testing points format is incorrect.")

    def calculate_error(self, latex_expression, points):
        error_sum = 0
        for point in points:
            x, expected_y = point
            obj = ExpressionEvaluator()
            formatted_latex = obj.remove_format_keywords(latex_expression)
            calculated_y = ExpressionEvaluator().evaluate_latex(formatted_latex, x)
            error_sum += abs(expected_y - calculated_y)
        return error_sum

    def create(self, request, *args, **kwargs):
        try:
            latex_expression, round_id, user_info, state, bidding_amount = self.get_required_data(request)
            round_info, points = self.get_round_info(round_id, state)
            error_sum = self.calculate_error(latex_expression, ast.literal_eval(points))

            if state == 'test' and int(round_id) > 1:
                ErrorInfo.objects.create(
                    user_info=user_info,
                    round=round_info,
                    error=error_sum,
                    submitted_function=latex_expression,
                    bidding_amount=bidding_amount,
                )
                data = {"message": "Backend testing started!"}
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": str(error_sum)}, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "Error while calculating!", "detail": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeductCreditsView(APIView):
    permission_classes = (IsAdminUser,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    def post(self, request, *args, **kwargs):
        round_id = request.data.get('round_id')
        if not round_id:
            return Response({"detail": "round_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            round_info = RoundInfo.objects.get(id=round_id)
        except RoundInfo.DoesNotExist:
            return Response({"detail": "Round not found."}, status=status.HTTP_404_NOT_FOUND)

        errors = list(ErrorInfo.objects.filter(round=round_info).values_list('user_info_id', 'error', 'bidding_amount'))

        if not errors:
            return Response({"detail": f"No errors found for round {round_id}."}, status=status.HTTP_404_NOT_FOUND)

        errors.sort(key=lambda x: x[1])

        min_error = errors[0][1]
        max_error = errors[-1][1]

        for user_info_id, error, bidding_amount in errors:
            normalized_error = (-0.25) + (error - min_error) * (0.5) / (max_error - min_error + 1e-5)

            user_info = UserInfo.objects.get(id=user_info_id)
            user_info.credits = user_info.credits - (normalized_error * bidding_amount)
            user_info.save()

        return Response({"detail": "Credits updated based on errors."}, status=status.HTTP_200_OK)


class LatexToSimpleExpressionView(APIView):
    serializer_class = LatexSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    def post(self, request, *args, **kwargs):
        serializer = LatexSerializer(data=request.data)
        if serializer.is_valid():
            latex_expr = serializer.validated_data['latex_expr']
            try:
                simple_expr = ExpressionEvaluator().get_parsed_expr(latex_expr)
                return Response({"simple_expr": str(simple_expr)}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
