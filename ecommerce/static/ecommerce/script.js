function toggleCards() {
    const cardsContainer = document.querySelector('.cardsProduct .row');
    const button = document.querySelector('.showMore');

    if (cardsContainer.style.maxHeight === '390px' || cardsContainer.style.maxHeight === '') {
        cardsContainer.style.maxHeight = '1000px';
        button.textContent = 'Ver Menos';
    } else {
        cardsContainer.style.maxHeight = '390px';
        button.textContent = 'Ver Mais';
    }
}