from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from . import forms, models
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login, logout
import copy



class BasePerfil(View):

    def setup(self,*args, **kwargs):
        super().setup(*args, **kwargs)
        self.template_name = 'perfil/criar.html'
        self.perfil = None
        
        if self.request.user.is_authenticated:
            self.perfil = models.Perfil.objects.filter(
                usuario=self.request.user
                ).first()
            self.contexto = {
                'userform':forms.UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    email = self.request.user.email,
                    instance = self.request.user,
                ),
                'perfilform':forms.PerfilForm(
                    data=self.request.POST or None,
                    instance= self.perfil,
                    ),
                }
        
        else: 
            self.contexto = {
                'userform':forms.UserForm(
                    data=self.request.POST or None,
                    ),
                'perfilform':forms.PerfilForm(data=self.request.POST or None),
                }
        
        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'

        self.render = render(self.request, self.template_name, self.contexto)
        self.userform = self.contexto['userform']
        self.perfilform = self.contexto['perfilform']
        

    def get(self,*args, **kwargs):

        return self.render


class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            messages.error(
                self.request, 
                'Dados inválidos! Verifique o formulário e tente novamente.'
            )
            return self.render
        
        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        self.carrinho = copy.deepcopy(self.request.session.get('carrinho'),{})
        message = ''

        if self.request.user.is_authenticated:
            usuario = get_object_or_404(
                models.User, 
                username = self.request.user.username 
                )
            usuario.username= username
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.email = email
            message = 'alterado'

            if password:
                usuario.set_password(password)

            usuario.save()
           
            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

            
            message = 'criado'
        
        if password:
            autentica = authenticate(
                self.request,
                username = username,
                password = password
            )
            if autentica:
                login(self.request, user=usuario)

        messages.success(
            self.request,
            f'Usuário {message} com sucesso!'
        )

        self.request.session['carrinho']=self.carrinho
        self.request.session.save()

        return redirect('perfil:criar')


class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        

        if not username or not password:
            messages.error(self.request, 'Usuário ou senha inválido.')
            return redirect('perfil:criar')

        autentica = authenticate(
            self.request, 
            username = username, 
            password = password
            )
        
        if not autentica:
            messages.error(self.request, 'Usuário ou senha inválido.')
            return redirect('perfil:criar')
        
        usuario = get_object_or_404(
                models.User, 
                username = username 
                )
        perfil = models.Perfil.objects.filter(usuario = usuario).first()
        if self.request.session.get('carrinho'):
            perfil.carrinho = copy.deepcopy(self.request.session.get('carrinho'),{})
            perfil.save()

        login(self.request, usuario)
        if perfil.carrinho:
            self.request.session['carrinho'] = perfil.carrinho
            self.request.session.save()
        messages.success(self.request, 'Logado com sucesso')
        return redirect('produto:lista')


class Logout(View):
    def get(self,*args, **kwargs):
        usuario = get_object_or_404(
                models.User, 
                username = self.request.user 
                )
        perfil = models.Perfil.objects.filter(usuario = usuario).first()
        
        perfil.carrinho = copy.deepcopy(self.request.session.get('carrinho'),{})

        if perfil.carrinho:
            perfil.save()

        logout(self.request)
        
        messages.success(self.request, 'Usuário deslogado.')
        return redirect('produto:lista')
    
class DispatchLoginRequired(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Usuário não está logado!'
            )
            return redirect('perfil:criar')
        return super().dispatch( *args, **kwargs)
        
    def get_queryset(self):
        perfil = models.Perfil.objects.filter(usuario=self.request.user).first()
        qs = super().get_queryset()
        qs = qs.filter(usuario = perfil)
        return qs
    

class ListaEnderecos(DispatchLoginRequired, ListView):
    template_name = 'perfil/lista_endereco.html'
    model = models.Endereco
    context_object_name = 'enderecos'
    paginate_by = 6
    ordering = ['-id']


class ModificarEndereco(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        
        if request.user.is_authenticated:
            endereco_id = self.kwargs.get("pk")
            self.perfil = get_object_or_404(
                models.Perfil, usuario = request.user)
            self.endereco = get_object_or_404(
                models.Endereco, pk = endereco_id)

            self.contexto = {
                'enderecoform':forms.EnderecoForm(
                        data=self.request.POST or None,
                        instance=self.endereco
                    ),
            }

        else:
            self.contexto={
                'enderecoform':forms.EnderecoForm(
                        data=self.request.POST or None,
                    ),
            }

        self.enderecoform = self.contexto[ 'enderecoform']
        self.render = render(self.request, 'perfil/endereco.html', self.contexto)

    

    def post(self,*args, **kwargs):
        if not self.enderecoform.is_valid():
            messages.error(
                self.request,
                'Dados inválidos! Verifique o formulário e tente novamente.'
            )
        
        messages.success(
            self.request,
            'Endereço alterado com sucesso!'
        )
        endereco = self.enderecoform.save(commit=False)
        endereco.usuario = self.perfil
        endereco.save()

        return redirect('perfil:enderecos')
    
    def get(self,*args, **kwargs):
        
        return self.render
    

class CriarEndereco(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.perfil = get_object_or_404(
            models.Perfil, usuario = request.user)
        
        self.contexto = {
            'enderecoform':forms.EnderecoForm(
                    data=self.request.POST or None,
                ),
        }

        self.enderecoform = self.contexto[ 'enderecoform']
        self.render = render(self.request, 'perfil/endereco.html', self.contexto)

    

    def post(self,*args, **kwargs):
        if not self.enderecoform.is_valid():
            messages.error(
                self.request,
                'Dados inválidos! Verifique o formulário e tente novamente.'
            )
        
        
        endereco = self.enderecoform.save(commit=False)
        endereco.usuario = self.perfil
        endereco.save()
        messages.success(
            self.request,
            'Endereço criado com sucesso!'
        )

        return redirect('perfil:enderecos')
    
    def get(self,*args, **kwargs):
        return self.render
    