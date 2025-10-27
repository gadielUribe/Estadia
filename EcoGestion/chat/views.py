from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from usuario.models import Usuario

@login_required
def chat_general(request):
    return render(request, 'chat/chat_general.html', {"section": "chat_general"})

@login_required
def chat_privado_selector(request):
    usuarios = Usuario.objects.exclude(id_usuario=request.user.id_usuario)
    return render(request, 'chat/chat_privado_selector.html', {
        'usuarios': usuarios,
        'section': 'chat_privado',
    })

@login_required
def chat_privado(request, receptor_id):
    receptor = get_object_or_404(Usuario, id_usuario=receptor_id)
    if receptor.id_usuario == request.user.id_usuario:
        from django.shortcuts import redirect
        return redirect('chat_privado_selector')
    usuarios = Usuario.objects.exclude(id_usuario=request.user.id_usuario)
    return render(request, 'chat/chat_privado.html', {
        'receptor': receptor,
        'usuarios': usuarios,
        'section': 'chat_privado',
    })
