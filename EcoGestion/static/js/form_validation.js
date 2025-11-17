(function(){
  function setMessage(field){
    if (field.validity.valueMissing){
      return field.dataset.requiredMsg || 'Por favor completa este campo.';
    }
    if (field.validity.typeMismatch){
      return field.dataset.typeMsg || 'Formato inválido.';
    }
    if (field.validity.patternMismatch){
      return field.dataset.patternMsg || 'El formato no coincide con lo esperado.';
    }
    if (field.validity.tooShort){
      return field.dataset.shortMsg || 'El valor es demasiado corto.';
    }
    if (field.validity.tooLong){
      return field.dataset.longMsg || 'El valor es demasiado largo.';
    }
    if (field.validity.rangeUnderflow){
      return field.dataset.minMsg || 'El valor es demasiado pequeño.';
    }
    if (field.validity.rangeOverflow){
      return field.dataset.maxMsg || 'El valor es demasiado grande.';
    }
    return '';
  }

  document.addEventListener('DOMContentLoaded', function(){
    var fields = document.querySelectorAll('input, textarea, select');
    fields.forEach(function(field){
      field.addEventListener('invalid', function(ev){
        var msg = setMessage(field);
        field.setCustomValidity(msg);
      });
      field.addEventListener('input', function(){
        field.setCustomValidity('');
      });
    });
  });
})();
