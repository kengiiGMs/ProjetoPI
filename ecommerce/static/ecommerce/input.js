const customNum = document.querySelectorAll('.custom-num');

customNum.forEach(num => {
    const numInput = num.querySelector('.num-input');
    const arrLeft = num.querySelector('.fa-angle-left');
    const arrRight = num.querySelector('.fa-angle-right');

    arrRight.addEventListener('click', () =>{
        numInput.stepUp();
    })

    arrLeft.addEventListener('click', () =>{
        numInput.stepDown();
    })
})
