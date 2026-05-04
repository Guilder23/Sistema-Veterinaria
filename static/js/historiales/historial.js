// Historial Clínico specific functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Módulo de Historial Clínico cargado');
    
    // Auto-expand textareas
    const textareas = document.querySelectorAll('textarea.form-control');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });
});
