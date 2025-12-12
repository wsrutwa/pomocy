
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Book, Osoba, Stanowisko
from .serializers import BookSerializer, OsobaSerializer, StanowiskoSerializer
from .forms import OsobaForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout


# określamy dostępne metody żądania dla tego endpointu
@api_view(['GET', "POST"])
def book_list(request):
    """
    Lista wszystkich obiektów modelu Book.
    """
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def book_list(request):
    """
    Lista wszystkich obiektów modelu Book.
    """
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def book_detail(request, pk):

    """
    :param request: obiekt DRF Request
    :param pk: id obiektu Book
    :return: Response (with status and/or object/s data)
    """
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    """
    Zwraca pojedynczy obiekt typu Book.
    """
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)


@api_view(['PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def book_update_delete(request, pk):

    """
    :param request: obiekt DRF Request
    :param pk: id obiektu Book
    :return: Response (with status and/or object/s data)
    """
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET","POST","DELETE"])
def osoba_detail(request, pk):
    try:
        osoba = Osoba.objects.get(pk=pk)
    except Osoba.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = OsobaSerializer(osoba)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = OsobaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        osoba.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(["GET"])
def osoba_list(request):
    if request.method == "GET":
        return Response(OsobaSerializer(Osoba.objects.all(),
                                        many = True).data,
                        status = status.HTTP_200_OK)
        
@api_view(["GET"])
def osoba_name_filter_url(request, name):
    if request.method == "GET":
        return Response(OsobaSerializer(Osoba.objects.filter(nazwisko__icontains = name),
                                        many = True).data,
                        status = status.HTTP_200_OK)
        
@api_view(["GET"])
def osoba_name_filter_params(request):
    if request.method == "GET":
        # Pobranie parametru 'name' z query params
        name = request.query_params.get('name', None)
        if name is not None:
            return Response(OsobaSerializer(Osoba.objects.filter(nazwisko__icontains = name),
                                            many = True).data,
                            status = status.HTTP_200_OK)
        else:
            return Response({"error": "Parametr 'name' jest wymagany."}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(["GET","POST","DELETE"])
def stanowisko_detail(request, pk):
    try:
        stanowisko = Stanowisko.objects.get(pk=pk)
    except Stanowisko.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = StanowiskoSerializer(stanowisko)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = StanowiskoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        stanowisko.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(["GET"])
def stanowisko_list(request):
    if request.method == "GET":
        return Response(StanowiskoSerializer(Stanowisko.objects.all(),
                                        many = True).data,
                        status = status.HTTP_200_OK)
        


from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter

class BookListView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# 1. Wyświetlanie, dodawanie i usuwanie pojedynczego obiektu Osoba
class OsobaDetailAPIView(RetrieveDestroyAPIView, CreateAPIView):
    queryset = Osoba.objects.all()
    serializer_class = OsobaSerializer

# 2. Wyświetlanie listy wszystkich obiektów Osoba
class OsobaListAPIView(ListAPIView):
    queryset = Osoba.objects.all()
    serializer_class = OsobaSerializer

# 3. Wyświetlanie listy osób po fragmencie nazwiska
class OsobaSearchAPIView(ListAPIView):
    serializer_class = OsobaSerializer

    def get_queryset(self):
        # Pobieramy parametr 'name' z URL
        name = self.kwargs.get('name', None)
        if name:
            return Osoba.objects.filter(nazwisko__icontains=name)
        return Osoba.objects.none()  # jeśli brak parametru, zwracamy pusty queryset
    
class OsobaNameFilterView(APIView):
    # #Prostsza wersja ale wtedy wpisujemy po ?search= zamiast ?name=
    # queryset = Osoba.objects.all()
    # serializer_class = OsobaSerializer
    # filter_backends = [SearchFilter]
    # search_fields = ['nazwisko']
    def get(self, request):
        # Pobranie parametru 'name' z query params
        name = request.query_params.get('name', None)

        if name:
            osoby = Osoba.objects.filter(nazwisko__icontains=name)
            serializer = OsobaSerializer(osoby, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Parametr 'name' jest wymagany."}, status=status.HTTP_400_BAD_REQUEST)

# 4. Wyświetlanie, dodawanie i usuwanie pojedynczego obiektu Stanowisko
class StanowiskoDetailAPIView(RetrieveDestroyAPIView, CreateAPIView):
    queryset = Stanowisko.objects.all()
    serializer_class = StanowiskoSerializer

# 5. Wyświetlanie listy wszystkich obiektów Stanowisko
class StanowiskoListAPIView(ListAPIView):
    queryset = Stanowisko.objects.all()
    serializer_class = StanowiskoSerializer
    
# kod umieszczamy w pliku views.py wybranej aplikacji

from django.http import HttpResponse
import datetime
from django.contrib.auth.decorators import login_required

def welcome_view(request):
    now = datetime.datetime.now()
    html = f"""
        <html><body>
        Witaj użytkowniku! </br>
        Aktualna data i czas na serwerze: {now}.
        </body></html>"""
    return HttpResponse(html)

@login_required(login_url='user-login')
def osoba_list_html(request):
    # pobieramy wszystkie obiekty Osoba z bazy poprzez QuerySet
    osoby = Osoba.objects.all()
    # return HttpResponse(osoby)
    return render(request,
                  "biblioteka/osoba/list.html",
                  {'osoby': osoby})
    
from django.http import Http404
    
def osoba_detail_html(request, id):
    # pobieramy konkretny obiekt Osoba
    try:
        osoba = Osoba.objects.get(id=id)
    except Osoba.DoesNotExist:
        raise Http404("Obiekt Osoba o podanym id nie istnieje")

    if request.method == "GET":
        return render(request,
                    "biblioteka/osoba/detail.html",
                    {'osoba': osoba})
    if request.method == "POST":
        osoba.delete()
        return redirect('osoba-list') 
    
def osoba_create_html(request):
    stanowiska = Stanowisko.objects.all()  # pobieramy listę stanowisk z bazy

    if request.method == "GET":
        return render(request, "biblioteka/osoba/create.html", {'stanowiska': stanowiska})
    elif request.method == "POST":
        imie = request.POST.get('imie')
        nazwisko = request.POST.get('nazwisko')
        plec = request.POST.get('plec')
        stanowisko_id = request.POST.get('stanowisko')

        if imie and nazwisko and plec and stanowisko_id:
            # pobieramy obiekt stanowiska
            try:
                stanowisko_obj = Stanowisko.objects.get(id=stanowisko_id)
            except Stanowisko.DoesNotExist:
                error = "Wybrane stanowisko nie istnieje."
                return render(request, "biblioteka/osoba/create.html", {'error': error, 'stanowiska': stanowiska})

            # tworzymy nową osobę
            Osoba.objects.create(
                imie=imie,
                nazwisko=nazwisko,
                plec=plec,
                stanowisko=stanowisko_obj
            )
            return redirect('osoba-list')
        else:
            error = "Wszystkie pola są wymagane."
            return render(request, "biblioteka/osoba/create.html", {'error': error, 'stanowiska': stanowiska})
        
def osoba_create_django_form(request):
    if request.method == "POST":
        form = OsobaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('osoba-list')  
    else:
        form = OsobaForm()

    return render(request,
                  "biblioteka/osoba/create_django.html",
                  {'form': form})
    
# Lab 8 (B)
## Zad 1
def book_list_html(request):
    books = Book.objects.all()
    return render(request,
                "biblioteka/book/list.html",
                {'books': books})
    
def stanowisko_list_html(request):
    stanowiska = Stanowisko.objects.all()
    return render(request,
                "biblioteka/stanowisko/list.html",
                {'stanowiska': stanowiska})
    
def book_detail_html(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        raise Http404("Obiekt Book o podanym id nie istnieje")

    if request.method == "GET":
        return render(request,
                    "biblioteka/book/detail.html",
                    {'book': book})
    ## Zad 4
    if request.method == "POST":
        book.delete()
        return redirect('book-list') 
    
def stanowisko_detail_html(request, id):
    try:
        stanowisko = Stanowisko.objects.get(id=id)
    except Stanowisko.DoesNotExist:
        raise Http404("Obiekt Stanowisko o podanym id nie istnieje")

    if request.method == "GET":
        return render(request,
                    "biblioteka/stanowisko/detail.html",
                    {'stanowisko': stanowisko})
    ## Zad 4
    if request.method == "POST":
        stanowisko.delete()
        return redirect('stanowisko-list') 
    
## Zad 2
from .forms import BookForm, StanowiskoForm
    
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book-list')  
    else:
        form = BookForm()

    return render(request,
                  "biblioteka/book/create.html",
                  {'form': form})
    
def stanowisko_create(request):
    if request.method == "POST":
        form = StanowiskoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stanowisko-list')  
    else:
        form = StanowiskoForm()

    return render(request,
                  "biblioteka/stanowisko/create.html",
                  {'form': form})
    
## Zad 3
def osoba_name_search(request):
    if request.method == "POST":
        nazwisko = request.POST.get("nazwisko")
        if nazwisko:
            osoby = Osoba.objects.filter(nazwisko__icontains = nazwisko)
            return render(request,
                "biblioteka/osoba/search.html",
                {'osoby': osoby})
    return render(request,
        "biblioteka/osoba/search.html")
    
## Zad 5
from django.shortcuts import get_object_or_404

def osoba_edit(request, id):
    osoba = get_object_or_404(Osoba, id = id)
    if request.method == 'POST':
        form = OsobaForm(request.POST, instance=osoba)  # bindujemy dane do istniejącego obiektu
        if form.is_valid():
            form.save() 
            return redirect('osoba-detail', id)  # przekierowujemy do widoku szczegółowego z id
    else:
        form = OsobaForm(instance=osoba)  # formularz z aktualnymi danymi obiektu

    return render(request, 'biblioteka/osoba/edit.html', {'form': form, 'osoba': osoba})

# A Stanowisko i Book adekwatnie do przykładu wyżej ;)

# ============= Lab 9 ================

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Hello, authenticated user!"})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('osoba-list')
        else:
            return render(request, 'biblioteka/login.html', {'error': 'Nieprawidłowe dane'})
    return render(request, 'biblioteka/login.html')

def user_logout(request):
    logout(request)
    return redirect('user-login')

from rest_framework.authtoken.models import Token

def drf_token_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            # zapisujemy token w sesji
            request.session['token'] = token.key
            request.session['user_id'] = user.id
            return redirect('osoba-list')
        else:
            return render(request, 'biblioteka/login.html', {'error': 'Nieprawidłowe dane'})
    return render(request, 'biblioteka/login.html')

def drf_token_logout(request):
    request.session.flush()
    return redirect('drf-token-login')

from functools import wraps

def drf_token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token_key = request.session.get('token')
        if not token_key:
            return redirect('drf-token-login')
        try:
            Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return redirect('drf-token-login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
