from rest_framework.routers import SimpleRouter

from library.apps import LibraryConfig

from library.views import AuthorViewSet, BookViewSet

app_name = LibraryConfig.name

router = SimpleRouter()
router.register(r"authors", AuthorViewSet, basename="author")
router.register(r"books", BookViewSet, basename="book")

url_patterns = []
urlpatterns = router.urls + url_patterns
