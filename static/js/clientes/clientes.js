// Clientes specific functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Módulo de Clientes cargado');
    
    // Example: Confirm deletion
    const deleteBtns = document.querySelectorAll('.btn-action.delete');
    deleteBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            // If it's not a link to the delete page, handle it here
            // But currently they are links to a confirmation page
        });
    });
});
