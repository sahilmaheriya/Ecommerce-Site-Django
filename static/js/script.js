
$('#menu').click(function(){
    $(this).toggleClass('fa-times');
    $('.nav-list').toggleClass('nav-active');
})

$('#prod_id').click(function(){
    let sid = $(this).attr('data-sid')
    let csr = $('input[name=csrfmiddlewaretoken]').val()
    mydata = {id:sid, csrfmiddlewaretoken:csr}
    $.ajax({
        url:'/add-to-cart/',
        method:'POST',
        data: mydata,
        success: function(data){
            console.log(data);
            $('#addtocart').html(`<a href="/cart/" class="btn btn-primary btn-lg p-3 fs-4 shadow w-50" id="go_to_cart">Go to cart</a>`)
            $('#buynow').addClass('d-none')
        }
    })
})


$('.plus-cart').click(function(){
    console.log('hello');
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[2]
    $.ajax({
        type:'GET',
        url:'/plus_cart',
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('total_amount').innerText = data.total_amount
        }
    })
})


$('.minus-cart').click(function(){
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[2]

    $.ajax({
        type:'GET',
        url:'/minus_cart',
        data:{
            prod_id:id
        },
        success:function(data){
            document.getElementById('quantity').innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('total_amount').innerText = data.total_amount
        }
    })
})



$('.remove-cart').click(function(){
    var id = $(this).attr('pid').toString();
    var eml = this

    $.ajax({
        type:'GET',
        url:'/remove_cart',
        data:{
            prod_id:id
        },
        success:function(data){
            document.getElementById('amount').innerText = data.amount
            document.getElementById('total_amount').innerText = data.total_amount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})





const url = window.location.href
const searchForm = document.getElementById('search-form')
const searchInput = document.getElementById('search-input')
const resultBox = document.getElementById('result-box')

console.log(resultBox.classList);
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const sendSearchData = (product) => {
    $.ajax({
        type:'POST',
        url: '/search_product/',
        data:{
            'csrfmiddlewaretoken':csrf,
            'product':product
        },
        success: (res) => {
            console.log(res.data);
            const data = res.data
            console.log(data);
            if(Array.isArray(data)){
                resultBox.innerHTML = ""
                data.forEach(product => {
                    resultBox.innerHTML += 
                    `<a href="/products_detail/${product.pk}">
                        <div class="row mt-2 mb-2 justify-content-center align-items-center">
                            <div class="col-2">
                                <img src="${product.product_image}" class="img-fluid product-image">
                            </div>
                            <div class="col-8">
                                <h5 class="product-title fs-3">${product.title}</h5>
                            </div>
                        </div>
                    </a>
                    <hr>
                    `
                })
            }
            else{
                if(searchInput.value.length > 0){
                    resultBox.innerHTML = 
                    `<b>${data}</b>`
                }
                else{
                    resultBox.classList.add('not-visible')
                }
            }
        },
        error: (err) => {
            console.log(err);
        }
    })
}

searchInput.addEventListener('keyup', e=>{
    console.log(e.target.value);

    if(resultBox.classList.contains('not-visible')){
        resultBox.classList.remove('not-visible')
    }

    sendSearchData(e.target.value)
})

