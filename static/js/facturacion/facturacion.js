// Facturación specific functionality
document.addEventListener('DOMContentLoaded', function() {
    const productsContainer = document.getElementById('products-container');
    const addProductBtn = document.getElementById('add-product');
    const totalDisplay = document.getElementById('total-amount');

    function calculateTotal() {
        let total = 0;
        const rows = document.querySelectorAll('.product-row');
        rows.forEach(row => {
            const select = row.querySelector('select');
            const qtyInput = row.querySelector('input[type="number"]');
            
            if (select.value) {
                const option = select.options[select.selectedIndex];
                const price = parseFloat(option.dataset.price || 0);
                const qty = parseInt(qtyInput.value || 0);
                total += price * qty;
            }
        });
        totalDisplay.textContent = total.toFixed(2);
    }

    if (addProductBtn) {
        addProductBtn.addEventListener('click', function() {
            const rows = document.querySelectorAll('.product-row');
            const newRow = rows[0].cloneNode(true);
            
            // Reset values
            newRow.querySelector('select').value = "";
            newRow.querySelector('input').value = "1";
            
            // Add remove button if it's not the first row
            if (!newRow.querySelector('.btn-remove-product')) {
                const removeBtn = document.createElement('button');
                removeBtn.type = 'button';
                removeBtn.className = 'btn-remove-product';
                removeBtn.innerHTML = '<i class="fas fa-times"></i>';
                removeBtn.addEventListener('click', function() {
                    newRow.remove();
                    calculateTotal();
                });
                newRow.appendChild(removeBtn);
            } else {
                newRow.querySelector('.btn-remove-product').addEventListener('click', function() {
                    newRow.remove();
                    calculateTotal();
                });
            }

            productsContainer.appendChild(newRow);
            
            // Add listeners to new elements
            newRow.querySelector('select').addEventListener('change', calculateTotal);
            newRow.querySelector('input').addEventListener('input', calculateTotal);
        });
    }

    // Initial listeners
    document.querySelectorAll('.product-row select').forEach(s => s.addEventListener('change', calculateTotal));
    document.querySelectorAll('.product-row input').forEach(i => i.addEventListener('input', calculateTotal));
});
