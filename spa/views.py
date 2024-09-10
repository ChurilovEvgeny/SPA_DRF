from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from spa.models import Habit, Place, Action
from spa.paginators import CustomPagePagination
from spa.serializers import HabitSerializer, PlaceSerializer, ActionSerializer
from users.permissions import IsOwner


class PlaceViewSet(viewsets.ModelViewSet):
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()


class ActionViewSet(viewsets.ModelViewSet):
    serializer_class = ActionSerializer
    queryset = Action.objects.all()


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)
        habit.set_next_execution_time()
        habit.save()


class HabitListAPIView(generics.ListAPIView):
    """View List для просмотра своих привычек"""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = CustomPagePagination
    queryset = Habit.objects.all().order_by("id")

    def get_queryset(self):
        # возврат кверисета для текущего пользователя
        return self.queryset.filter(user=self.request.user)


class HabitPublicListAPIView(generics.ListAPIView):
    """View List для просмотра ВСЕХ публичных привычек"""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagePagination
    queryset = Habit.objects.all().filter(is_public=True).order_by("id")


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_update(self, serializer):
        habit = serializer.save()
        habit.set_next_execution_time()
        habit.save()


class HabitDeleteAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
