from django.forms import ModelForm
from django import forms
from perfil.models import Perfil, Endereco
from django.contrib.auth.models import User

class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'
        exclude = ('usuario','carrinho')

class EnderecoForm(ModelForm):
    class Meta:
        model = Endereco
        fields = '__all__'
        exclude = ('usuario',)

class UserForm(ModelForm):
    password = forms.CharField(
        required=False,
        widget = forms.PasswordInput(),
        label = 'Senha'
        )
    
    password2 = forms.CharField(
        required=False,
        widget = forms.PasswordInput(),
        label = 'Confirme sua senha'
        )
    def __init__(self, usuario = None, email = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario
        self.email = email
        

    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password',
                'password2')

    def clean(self, *args, **kwargs):
        cleaned = self.cleaned_data
        validation_error_messages = {}

        usuario_data = cleaned.get('username')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')
        email_data = cleaned.get('email')

        user_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()
        
        error_message_user_exists = 'Usuário já cadastrado!'
        error_message_email_exists = 'Endereço de e-mail já cadastrado!'
        error_message_password_match = 'As senhas não coincidem!'
        error_message_password_short = 'Insira uma senha com 6 ou mais caracteres!'
        error_message_field_is_required = 'Este campo é obrigatório!'
        

        if self.usuario:
            if self.usuario.username != usuario_data:
                if user_db:
                    validation_error_messages['username'] = error_message_user_exists
            
            if self.email != email_data:
                if email_db:
                    validation_error_messages['email'] = error_message_email_exists

            if password_data:

                if password_data != password2_data:
                    validation_error_messages['password2']=error_message_password_match

                if len(password_data) < 6:
                    validation_error_messages['password']=error_message_password_short  
            
        else:
            if user_db:
                validation_error_messages['username'] = error_message_user_exists
            
            if email_db:
                validation_error_messages['email'] = error_message_email_exists

            if password_data != password2_data:
                validation_error_messages['password2']=error_message_password_match

            if len(password_data) < 6:
                validation_error_messages['password']=error_message_password_short 

        if validation_error_messages:
            raise (forms.ValidationError(validation_error_messages))