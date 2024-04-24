from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post,UserProfile,Category
from .forms import PostForm, ProfileForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm,RegisterForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .tasks import send_notification_email


def categories_list(request):
    categories = Category.objects.all()  # Получение всех категорий из базы данных
    return render(request, 'categories_list.html', {'categories': categories})




@login_required
def become_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('author_granted')  # Redirect to a confirmation page or home


def author_granted(request):
    return render(request, 'author_granted.html')


def search(request):
    query_set = Post.objects.filter(post_type='NE')  # Исходно фильтруем только новости

    # Получаем значения из параметров запроса
    title = request.GET.get('title')
    author_name = request.GET.get('author')
    date_from = request.GET.get('date_from')

    # Фильтрация по названию
    if title:
        query_set = query_set.filter(title__icontains=title)

    # Фильтрация по имени автора
    if author_name:
        query_set = query_set.filter(author__user__username__icontains=author_name)

    # Фильтрация по дате
    if date_from:
        query_set = query_set.filter(created_at__date__gte=date_from)

    return render(request, 'search.html', {'news': query_set})


def home(request):
    return render(request, 'home.html')

def news_list(request):
    news = Post.objects.filter(post_type='NE').order_by('-created_at')
    paginator = Paginator(news, 10)  # Показывать по 10 новостей на странице.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news_list.html', {'page_obj': page_obj})

def article_detail(request, article_id):
    # Получаем статью по ID или возвращаем страницу 404, если статья не найдена
    article = get_object_or_404(Post, pk=article_id)
    return render(request, 'news_detail.html', {'article': article})


# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     form_class = PostForm
#     template_name = 'post_form.html'
#     success_url = reverse_lazy('news_list')
#
#
#     def form_valid(self, form):
#         # Задаем post_type на основе переданного параметра, или используем значение по умолчанию 'NE'
#         form.instance.post_type = self.kwargs.get('post_type', 'NE')
#         return super(PostCreateView, self).form_valid(form)
#
#
# class PostUpdateView(UpdateView,LoginRequiredMixin):
#     model = Post
#     form_class = PostForm
#     template_name = 'post_form.html'
#     success_url = reverse_lazy('news_list')
#
#
# class PostDeleteView(DeleteView,LoginRequiredMixin):
#     model = Post
#     template_name = 'post_confirm_delete.html'
#     success_url = reverse_lazy('news_list')
#
# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     form_class = PostForm
#     template_name = 'post_form.html'
#     success_url = reverse_lazy('news_list')
#
#
#     def form_valid(self, form):
#         # Задаем post_type на основе переданного параметра, или используем значение по умолчанию 'NE'
#         form.instance.post_type = self.kwargs.get('post_type', 'NE')
#         return super(PostCreateView, self).form_valid(form)
#
#
# class PostUpdateView(UpdateView,LoginRequiredMixin):
#     model = Post
#     form_class = PostForm
#     template_name = 'post_form.html'
#     success_url = reverse_lazy('news_list')
#
#
# class PostDeleteView(DeleteView,LoginRequiredMixin):
#     model = Post
#     template_name = 'post_confirm_delete.html'
#     success_url = reverse_lazy('news_list')
#


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('news_list')  # Redirect to the news list after creation
    permission_required = 'news_list.add_post'  # Adjust the permission name based on your model's app_label

    def form_valid(self, form):
        form.instance.author = self.request.user  # Automatically set the author to the current user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('news_list')  # Redirect after updating
    permission_required = 'news_list.change_post'  # Ensure the correct permission

    def get_queryset(self):
        """
        This method ensures that a user can only edit their own posts unless they have special permissions.
        """
        queryset = super().get_queryset()
        if not self.request.user.has_perm('your_app.change_any_post'):
            queryset = queryset.filter(author=self.request.user)
        return queryset


@permission_required('news_list.add_post', raise_exception=True)
def create_post(request, post_type):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.post_type = post_type
            post.save()
            return redirect('news_list')
    else:
        form = PostForm(initial={'post_type': post_type})
    return render(request, 'post_form.html', {'form': form})

@login_required
def edit_post(request, pk, post_type):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.post_type = post_type
            post.save()
            return redirect('news_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form})

@login_required
def delete_post(request, pk, post_type):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('news_list')




class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = ProfileForm
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('profile')  # Используйте reverse_lazy для динамических URL

    def get_object(self, queryset=None):
        """
        Возвращает объект профиля, который должен быть отредактирован.
        Это гарантирует, что пользователь может редактировать только свой профиль.
        """
        # Если queryset не предоставлен, используем базовый queryset модели
        if queryset is None:
            queryset = self.get_queryset()

        # Получаем профиль текущего пользователя, используя OneToOne связь с User
        return get_object_or_404(queryset, user=self.request.user)

    # Настройки для перенаправления и сообщений
    login_url = '/login/'
    redirect_field_name = 'next'

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Направление пользователя на главную страницу после входа
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print(form.fields)
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            send_notification_email(email, 'Welcome to our site!', f'Hi, {username}! Welcome to our site!')

            return redirect('login')  # Перенаправление на страницу входа после успешной регистрации
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.add(request.user)
    return redirect('categories_list')

@login_required
def unsubscribe_from_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.remove(request.user)
    return redirect('categories_list')



