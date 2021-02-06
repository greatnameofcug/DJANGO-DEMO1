from django.shortcuts import render

# Create your views here.
from catalog.models import Book, Author, BookInstance, Genre
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic

class BookListView(generic.ListView):
    model = Book
    
    ################这里教程又错了，两个变量名不匹配
    context_object_name = 'book_list'   # your own name for the list as a template variable

    queryset = Book.objects.all()

    ############################这教程就有毒，谁知道我又没有放一本带war的书！！！！！！！！！！！！！
    #queryset = Book.objects.filter(title__icontains='war')[:3] # Get 5 books containing the title war

    template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    '''
    def get_queryset(self):
        return Book.objects.all()#filter(title__icontains='war')[:3] # Get 5 books containing the title war
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context
    '''
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book


def book_detail_view(request, primary_key):
    try:
        book = Book.objects.get(pk=primary_key)
    except Book.DoesNotExist:
        raise Http404('Book does not exist')

    return render(request, 'catalog/book_detail.html', context={'book': book})

from django.shortcuts import get_object_or_404

def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})

class AuthorListView(generic.ListView):
    model = Author
    
    context_object_name = 'author_list'   # your own name for the list as a template variable
    queryset = Author.objects.all()
    #queryset = Book.objects.filter(title__icontains='war')[:3] # Get 5 books containing the title war
    template_name = 'authors/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    '''
    def get_queryset(self):
        return Book.objects.all()#filter(title__icontains='war')[:3] # Get 5 books containing the title war
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context
    '''
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author