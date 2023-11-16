document.addEventListener('DOMContentLoaded', function () {

    if (document.querySelector("#editrBtn")){
        document.querySelector("#editBtn").addEventListener("click", function(){
            this.remove();
            document.querySelector("#deleteBtn").remove()
            
            let nomeProdutoElement = document.querySelector("#nomeProduto");
            let nomeProdutoText = nomeProdutoElement.innerText;
            nomeProdutoElement.remove()
    
            let valorProdutoElement = document.querySelector("#valorProduto");
            let valorProdutoNumber = valorProdutoElement.innerText;
            valorProdutoElement.remove()
    
            // Input Nome Produto
            let nomeProdutoInput = document.createElement("input");
            nomeProdutoInput.setAttribute("type", "text");
            nomeProdutoInput.name = "novo_nome";
            nomeProdutoInput.className = "form-control border border-danger my-3";
            nomeProdutoInput.required = true;
            nomeProdutoInput.value = nomeProdutoText;
    
            // Input Valor Produto
            let valorProdutoInput = document.createElement("input");
            valorProdutoInput.setAttribute("type", "number");
            valorProdutoInput.name = "novo_valor";
            valorProdutoInput.className = "form-control border border-danger mb-3";
            valorProdutoInput.value = parseFloat(valorProdutoNumber);
            valorProdutoInput.required = true;
            valorProdutoInput.min = 0;
            valorProdutoInput.step = .01;
    
            let submitBtn = document.createElement("button")
            submitBtn.setAttribute("type", "submit");
            submitBtn.innerHTML = "Editar";
            submitBtn.className = "btn btn-outline-danger";
            submitBtn.style.borderRadius = "0px";
    
            document.querySelector("#nomeProdutoDiv").append(nomeProdutoInput);
            document.querySelector("#valorProdutoDiv").append(valorProdutoInput);
            document.querySelector("#submitBtnDiv").append(submitBtn);
        })
    }

    // Mostar quantidade de produtos restante em um determinado tamanho.
    const spanTamanho = document.querySelector("#spanTamanho");
    const inputQuantidade = document.querySelector("#inputQuantity");

    document.querySelectorAll(".tamanho-btn").forEach(btn => {
        
        if (btn.id === "tamanho_p" && produto.tamanhoP == 0) {
            btn.disabled = true;
            document.querySelector("#label_p").className = "disabled-btn btn btn-outline-danger";
        } 
        
        else if (btn.id === "tamanho_m" && produto.tamanhoM == 0) {
            btn.disabled = true;
            document.querySelector("#label_m").className = "disabled-btn btn btn-outline-danger";
        } 
        
        else if (btn.id === "tamanho_g" && produto.tamanhoG == 0) {
            btn.disabled = true
            document.querySelector("#label_g").style.cssText = "disabled-btn btn btn-outline-danger";
        } 
        
        else if (btn.id === "tamanho_gg" && produto.tamanhoGG == 0) {
            btn.disabled = true;
            document.querySelector("#label_gg").style.cssText = "disabled-btn btn btn-outline-danger";
        }

        btn.addEventListener("click", function(){

            switch (btn.id){
                case "tamanho_p":
                    spanTamanho.innerText = `Produtos Restantes: ${produto.tamanhoP}`;
                    // Limitar a quantidade de produtos q o cliente pode comprar
                    // à quantidade restante do produto de tal tamanho.
                    inputQuantidade.max = produto.tamanhoP;
                    break;

                case "tamanho_m":
                    spanTamanho.innerText = `Produtos Restantes: ${produto.tamanhoM}`;
                    inputQuantidade.max = produto.tamanhoM;
                    break;
                
                case "tamanho_g":
                    spanTamanho.innerText = `Produtos Restantes: ${produto.tamanhoG}`;
                    inputQuantidade.max = produto.tamanhoG;
                    break;

                case "tamanho_gg":
                    spanTamanho.innerText = `Produtos Restantes: ${produto.tamanhoGG}`;
                    inputQuantidade.max = produto.tamanhoGG;
                    break;

            }
        })
    })


    // Review
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