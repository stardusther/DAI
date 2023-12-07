// se ejecuta recien cargada la página
document.addEventListener('DOMContentLoaded', async () => {
    const spanParaEstrellas = document.querySelectorAll('span.user-rating');
    const productElements = document.querySelectorAll('.product');
    const productIds = Array.from(productElements).map(element => element.dataset.productId);

    for (const productId of productIds) {
        try {
            const product = await getProductById(productId);
            const stars = generateStars(product.rating.rate); // Generar estrellas basadas en la calificación

            // Encontrar el elemento específico del producto y rellenarlo con las estrellas generadas
            const productElement = document.querySelector(`.product[data-product-id="${productId}"]`);
            const starContainer = productElement.querySelector('.rating');
            starContainer.innerHTML = stars;


        } catch (error) {
            console.error(`Error fetching product ${productId}:`, error);
        }
    }

    // Para llenar todos los user-rating con estrellas vacías
    const allStarContainers = document.querySelectorAll('.user-rating');
    allStarContainers.forEach(container => {
        container.innerHTML = generateEmptyStars();

        // Añadir evento de clic a cada estrella
        container.addEventListener('click', async (event) => {
            const clickedStar = event.target;

            if (clickedStar.classList.contains('fa-star') || clickedStar.classList.contains('fa-star-o')) {
                const stars = Array.from(container.children); // Obtener todas las estrellas en el contenedor
                const clickedIndex = stars.indexOf(clickedStar);

                // Llenar la estrella clicada y todas las anteriores
                for (let i = 0; i <= clickedIndex; i++) {
                    stars[i].classList.remove('fa-star-o');
                    stars[i].classList.add('fa-star');
                }

                // Vaciar las estrellas posteriores
                for (let i = clickedIndex + 1; i < stars.length; i++) {
                    stars[i].classList.remove('fa-star');
                    stars[i].classList.add('fa-star-o');
                }

                // Establecer el valor del rating
                const ratingValue = clickedIndex + 1; // El valor va de 1 a 5
                console.log('Rating:', ratingValue);

                const productId = container.closest('.product').dataset.productId;
                await updateRating(productId, ratingValue); // Llamar a la función para actualizar el rating en el servidor
            }
        });
    });
});

// Función para obtener un producto por su ID desde la API
async function getProductById(productId) {
    const response = await fetch(`/api/product/${productId}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch product ${productId}`);
    }
    return response.json();
}

// Función para generar las estrellas basadas en el rating
function generateStars(rate) {
    const filledStars = '<span class="fa fa-star"></span>'.repeat(Math.floor(rate));
    const halfStar = rate % 1 !== 0 ? '<span class="fa fa-star-half-o"></span>' : '';
    const emptyStars = '<span class="fa fa-star-o"></span>'.repeat(5 - Math.ceil(rate));
    return `${filledStars}${halfStar}${emptyStars}`;
}

// Función para generar estrellas vacías
function generateEmptyStars() {
    return '<span class="fa fa-star-o"></span>'.repeat(5);
}


async function updateRating(productId, ratingValue) {
    const csrftoken = getCookie('csrftoken'); // Obtener el token CSRF de la cookie

    const response = await fetch(`/api/product/${productId}/rating?rating=${ratingValue}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken // Agregar el token CSRF a los encabezados
        }
    });

    if (response.ok) {
        const successMessage = document.getElementById('successMessage');
        successMessage.style.display = 'block'; // Mostrar el mensaje
        setTimeout(() => {
            successMessage.style.display = 'none'; // Ocultar el mensaje después de unos segundos
        }, 3000); // Ocultar después de 3 segundos (ajusta el tiempo según necesites)
    } else {
        throw new Error('Failed to update rating');
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

