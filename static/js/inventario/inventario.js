// Inventario specific functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Módulo de Inventario cargado');
    
    const esMedicamentoCheckbox = document.getElementById('es_medicamento');
    const vencimientoGroup = document.getElementById('vencimiento-group');
    
    if (esMedicamentoCheckbox && vencimientoGroup) {
        // Toggle vencimiento based on es_medicamento
        const toggleVencimiento = () => {
            if (esMedicamentoCheckbox.checked) {
                vencimientoGroup.style.display = 'block';
            } else {
                vencimientoGroup.style.display = 'none';
            }
        };
        
        esMedicamentoCheckbox.addEventListener('change', toggleVencimiento);
        toggleVencimiento(); // Initial state
    }
});
