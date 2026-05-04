// Mascotas specific functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Módulo de Mascotas cargado');
    
    // Preview image before upload
    const fotoInput = document.getElementById('foto');
    if (fotoInput) {
        fotoInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Update preview if exists or log
                    console.log('Imagen cargada');
                }
                reader.readAsDataURL(this.files[0]);
            }
        });
    }
});
