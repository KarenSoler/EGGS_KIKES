document.addEventListener('DOMContentLoaded', () => {
    const baseUrl = 'http://127.0.0.1:8000/eggs';

    // Handle form submission for creating an egg
    document.getElementById('create-egg-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const type_egg = document.getElementById('type_egg').value;
    const price = parseFloat(document.getElementById('price').value);
    const supplier = document.getElementById('supplier').value;

    try {
        const response = await fetch('http://127.0.0.1:8000/eggs', {  // Asegúrate de usar la URL correcta
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ type_egg, price, supplier }),
        });

        if (!response.ok) {
            const data = await response.json();
            console.error('Error:', data.detail);  // Muestra el error detallado en la consola
        } else {
            const data = await response.json();
            console.log('Created Egg:', data);
            await fetchEggs(); // Refresca la lista de huevos
        }
    } catch (error) {
        console.error('Network Error:', error);  // Muestra el error de red en la consola
    }
});
    // Handle form submission for updating an egg
    document.getElementById('update-egg-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = parseInt(document.getElementById('update-id').value);
        const type_egg = document.getElementById('update-type_egg').value || undefined;
        const price = parseFloat(document.getElementById('update-price').value) || undefined;
        const supplier = document.getElementById('update-supplier').value || undefined;

        const response = await fetch(`${baseUrl}/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ type_egg, price, supplier }),
        });

        const data = await response.json();
        if (!response.ok) {
            console.error('Error:', data.detail);  // Muestra el error detallado en la consola
        } else {
            console.log('Updated Egg:', data);
            await fetchEggs(); // Refresca la lista de huevos
        }
    });

    // Handle button click to fetch all eggs
    document.getElementById('fetch-eggs').addEventListener('click', fetchEggs);

    // Function to fetch all eggs and update the list
    async function fetchEggs() {
        const response = await fetch(baseUrl);
        const data = await response.json();
        const eggsList = document.getElementById('eggs-list');
        eggsList.innerHTML = '';  // Clear the existing list

        data.forEach(egg => {
            const li = document.createElement('li');
            li.textContent = `ID: ${egg.id}, Type: ${egg.type_egg}, Price: ${egg.price}, Supplier: ${egg.supplier}`;
            eggsList.appendChild(li);
        });
    }
});