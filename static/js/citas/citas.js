// Citas specific functionality
document.addEventListener('DOMContentLoaded', function() {
    const fechaInput = document.getElementById('fecha');
    const vetSelect = document.getElementById('veterinario');
    const mascotaSelect = document.getElementById('mascota');
    const timeSlotsGrid = document.getElementById('time-slots');
    const timeSlotsContainer = document.getElementById('time-slots-container');
    const noDateSelected = document.getElementById('no-date-selected');
    const selectedHourInput = document.getElementById('selected-hour');
    const btnSubmit = document.getElementById('btn-submit');

    // Summary elements
    const summaryPet = document.getElementById('summary-pet');
    const summaryDate = document.getElementById('summary-date');
    const summaryHour = document.getElementById('summary-hour');

    // Set minimum date to today
    const today = new Date().toISOString().split('T')[0];
    fechaInput.setAttribute('min', today);

    function updateSummary() {
        summaryPet.textContent = mascotaSelect.options[mascotaSelect.selectedIndex]?.text.split('(')[0].trim() || '-';
        summaryDate.textContent = fechaInput.value || '-';
        summaryHour.textContent = selectedHourInput.value || '-';

        // Enable/disable submit button
        if (mascotaSelect.value && fechaInput.value && selectedHourInput.value) {
            btnSubmit.disabled = false;
        } else {
            btnSubmit.disabled = true;
        }
    }

    async function fetchAvailableHours() {
        const fecha = fechaInput.value;
        const vetId = vetSelect.value;

        if (!fecha) {
            timeSlotsContainer.style.display = 'none';
            noDateSelected.style.display = 'block';
            return;
        }

        try {
            const response = await fetch(`/citas/obtener-horas/?fecha=${fecha}&veterinario=${vetId}`);
            const data = await response.json();

            if (data.horas) {
                renderTimeSlots(data.horas);
                timeSlotsContainer.style.display = 'block';
                noDateSelected.style.display = 'none';
            }
        } catch (error) {
            console.error('Error fetching hours:', error);
        }
    }

    function renderTimeSlots(horas) {
        timeSlotsGrid.innerHTML = '';
        
        // Define all possible hours from 08:00 to 18:00
        const allHours = [];
        let curr = 8 * 60; // 8:00 in minutes
        const end = 18 * 60; // 18:00 in minutes

        while (curr < end) {
            const h = Math.floor(curr / 60);
            const m = curr % 60;
            const timeStr = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`;
            allHours.push(timeStr);
            curr += 30;
        }

        allHours.forEach(hour => {
            const slot = document.createElement('div');
            slot.className = 'time-slot';
            slot.textContent = hour;

            if (horas.includes(hour)) {
                slot.addEventListener('click', () => {
                    // Remove selected from others
                    document.querySelectorAll('.time-slot').forEach(s => s.classList.remove('selected'));
                    slot.classList.add('selected');
                    selectedHourInput.value = hour;
                    updateSummary();
                });
            } else {
                slot.classList.add('occupied');
                slot.title = 'No disponible';
            }

            timeSlotsGrid.appendChild(slot);
        });
    }

    fechaInput.addEventListener('change', () => {
        selectedHourInput.value = '';
        fetchAvailableHours();
        updateSummary();
    });

    vetSelect.addEventListener('change', () => {
        selectedHourInput.value = '';
        fetchAvailableHours();
    });

    mascotaSelect.addEventListener('change', updateSummary);
});
