document.addEventListener('DOMContentLoaded', function () {
    const mensagemErro = document.querySelector("#mensagem-erro");

    document.querySelector("#review-form").addEventListener("submit", function(event){
        if (document.querySelector("#starValue").value === ""){
            event.preventDefault();
            mensagemErro.style.display = "block";
        } else {
            mensagemErro.style.display = "none";
        }
    })

    const starWrapper = document.querySelector(".stars");
    const stars = document.querySelectorAll(".stars i");

    stars.forEach((star, clickedIdx) => {
        star.addEventListener('click', function () {
            starWrapper.classList.add("disabled")
            stars.forEach((otherStar, otherIdx) => {
                if (otherIdx <= clickedIdx) {
                    otherStar.classList.add("active");
                }
            })

            document.getElementById('starValue').value = clickedIdx + 1;
            
            if (mensagemErro.style.display === 'block'){
                mensagemErro.style.display = 'none'
            }

            console.log(`star of index ${clickedIdx} was clicked`)
        })
    })


});