document.addEventListener('DOMContentLoaded', function () {
    
  // Selecciona el modal por su ID
  var confirmDeleteModal = document.getElementById('confirmDeleteModal');
  
  // Asegurarnos de que el modal existe en esta página antes de continuar
  if (confirmDeleteModal) {

    // Escucha CADA VEZ que el modal esté a punto de mostrarse
    confirmDeleteModal.addEventListener('show.bs.modal', function (event) {
      
      // 'event.relatedTarget' es el botón "Eliminar" que fue presionado
      var button = event.relatedTarget;
      
      // Extrae la información de los atributos 'data-*' del botón
      var deleteUrl = button.getAttribute('data-delete-url');
      var userName = button.getAttribute('data-user-name');
      
      // --- Actualiza el contenido del modal ---
      
      // 1. Pone la URL correcta en el 'action' del formulario de confirmación
      var deleteForm = document.getElementById('deleteForm');
      deleteForm.setAttribute('action', deleteUrl);
      
      // 2. Pone el nombre del usuario en el cuerpo del modal
      var userNameElement = document.getElementById('userNameInModal');
      userNameElement.textContent = userName;
    });
  }
});