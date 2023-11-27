from rest_framework import routers
from .views import ExampleViewSet, FileUploadAPIView, FacilityViewSet, PieChartViewSet, MillViewSet, TableColumnViewSet, TTPViewSet, AgriplotViewSet, AgriplotResultViewSet, AgriplotResultWKTViewSet
from django.urls import path, include


router = routers.DefaultRouter()

router.register('facility', FacilityViewSet, basename='facility')
router.register('mill', MillViewSet, basename='mill')
router.register('ttp', TTPViewSet, basename='ttp')
router.register('agriplot', AgriplotViewSet, basename='agriplot')


urlpatterns = [
    path('', include(router.urls)),
    path('app/example', ExampleViewSet.as_view({'get': 'list'}),
         name='example-api'),
    path('upload-facility/', FileUploadAPIView.as_view(),
         name='upload-facility'),
    path('pie-chart/<section>/<distinct>/', PieChartViewSet.as_view(),
         name='pie-chart'),
    path('table-column/<section>/', TableColumnViewSet.as_view(),
         name='table-column'),
    path('agriplot-result/', AgriplotResultViewSet.as_view(),
         name='agriplot-result'),
    path('agriplot-result-wkt/', AgriplotResultWKTViewSet.as_view(),
         name='agriplot-result-wkt'),
]
