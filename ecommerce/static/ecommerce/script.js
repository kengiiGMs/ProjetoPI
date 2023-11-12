document.addEventListener('DOMContentLoaded', function () {
    const pSpan = document.querySelector("#span_p")
    const mSpan = document.querySelector("#span_m") 
    const gSpan = document.querySelector("#span_g") 
    const ggSpan = document.querySelector("#span_gg") 

    document.querySelectorAll(".tamanho-btn").forEach(btn => {
        btn.addEventListener("click", function(){

            switch (btn.id){
                case "tamanho_p":
                    pSpan.style.display = "block";
                    mSpan.style.display = "none";
                    gSpan.style.display = "none";
                    ggSpan.style.display = "none";
                    break;

                case "tamanho_m":
                    pSpan.style.display = "none";
                    mSpan.style.display = "block";
                    gSpan.style.display = "none";
                    ggSpan.style.display = "none";
                    break;
                
                case "tamanho_g":
                    pSpan.style.display = "none";
                    mSpan.style.display = "none";
                    gSpan.style.display = "block";
                    ggSpan.style.display = "none";
                    break;

                case "tamanho_gg":
                    pSpan.style.display = "none";
                    mSpan.style.display = "none";
                    gSpan.style.display = "none";
                    ggSpan.style.display = "block";
                    break;

            }
        })
    })


    const mensagemErro = document.querySelector("#mensagem-erro");
    
    if (document.querySelector("#review-form")){
        document.querySelector("#review-form").addEventListener("submit", function(event){
            if (document.querySelector("#starValue").value === ""){
                event.preventDefault();
                mensagemErro.style.display = "block";
            } else {
                mensagemErro.style.display = "none";
            }
        })
    }

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