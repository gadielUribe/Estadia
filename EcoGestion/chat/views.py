from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from usuario.models import Usuario

@login_required
def chat_general(request):
    return render(request, 'chat/chat_general.html')

@login_required
def chat_privado(request, receptor_id):
    receptor = get_object_or_404(Usuario, id_usuario=receptor_id)
    return render(request, 'chat/chat_privado.html', {'receptor': receptor})