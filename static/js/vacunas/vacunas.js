// Vacunas specific functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Módulo de Vacunas cargado');
    
    // Highlight next doses that are coming soon
    const nextDoseDates = document.querySelectorAll('.next-dose');
    const today = new Date();
    
    nextDoseDates.forEach(span => {
        const dateStr = span.textContent.split('/').reverse().join('-');
        const doseDate = new Date(dateStr);
        
        const diffTime = doseDate - today;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays <= 7 && diffDays > 0) {
            span.style.color = 'var(--warning-color)';
            span.title = '¡Próxima dosis pronto!';
        } else if (diffDays <= 0) {
            span.style.color = 'var(--danger-color)';
            span.title = '¡Dosis atrasada!';
        }
    });
});
