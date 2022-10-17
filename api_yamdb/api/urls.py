from api.views import reviews
from api.views.auth import SignUpViewSet, TokenViewSet
from api.views.users import UserViewSet
from django.urls import include, path
from rest_framework import routers

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('v1/users', UserViewSet, basename='users')
router_v1.register('v1/titles', reviews.TitleViewSet, basename='titles')
router_v1.register('v1/genres', reviews.GenreViewSet, basename='genres')
router_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews',
    reviews.ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    reviews.CommentViewSet,
    basename='comments'
)
router_v1.register(
    'v1/categories',
    reviews.CategoryViewSet,
    basename='categories'
)

urlpatterns = [
    path('v1/auth/signup/', SignUpViewSet.as_view()),
    path('v1/auth/token/', TokenViewSet.as_view()),
    path('', include(router_v1.urls)),
]
