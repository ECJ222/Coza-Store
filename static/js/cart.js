//getting data from Html Elements
var cart = document.getElementsByClassName('add-cart');

for (let i = 0; i < cart.length; i+=1){
	cart[i].addEventListener('click', function(){
		var productId = this.dataset.product;
		var action = this.dataset.action;
		console.log(action);
		if (action == 'add')
		{
			var size = document.getElementById("size").value;
			
			console.log(size);
			if ( size == "Choose an option" )
			{
				$(".swal-overlay").hide("swal-overlay--show-modal");
				document.getElementById("select").style.border = "1px solid red";
				document.getElementById("message1").innerHTML = "Please select from the available size <br/> options"; 
				
			}
			else
			{
				$(".swal-overlay").show("swal-overlay--show-modal");
				//document.getElementById("cart-pop").classList.add("js-addcart-detail");

				if (user == 'AnonymousUser')
				{	
					
					if (action == 'add')
					{
						addtoCart(productId,action,size);
					}
					
				}else
				{
					if (action == 'add')
					{
						addtoCart(productId,action,size);
					}
					
				}
			}
		}else if (action == 'remove')
		{
			removefromcart(productId,action);
		}

	})
}


//sending data to django
function addtoCart(productId,action,size,quantity){

	let url = '/apicart/'

	fetch(url, {
		method : 'POST',
		headers : {
			'Content-Type' : 'application/json',
			'X-CSRFToken' : csrftoken,
		},
		body : JSON.stringify({'productId' : productId , 'action' : action, 'size' : size, 'user':user  })
	}).then(response => {
		return response.json()
	}).then(data => {
			console.log(data);	
			setTimeout(()=>{
             location.reload()
        	},2000)
	})
}




//var removecart = document.getElementsByClassName('cart');
//console.log(removecart);



//sending data to Django to remove

function removefromcart(productId,action){

	let url = '/apicart/'

	fetch(url, {
		method : 'POST',
		headers : {
			'Content-Type' : 'application/json',
			'X-CSRFToken' : csrftoken,
		},
		body : JSON.stringify({'productId' : productId , 'action' : action})
	}).then(response => {
		return response.json()
	}).then(data => {
			console.log(data);	
			setTimeout(()=>{
             location.reload()
        	},2000)
	})
}

//Shopping Cart Functionality

var plus = document.getElementsByClassName('btn-num-product-up'); //+

var minus = document.getElementsByClassName('btn-num-product-down'); //-

for ( let i = 0; i < plus.length; i+=1){
	plus[i].addEventListener('click', function(){
		var operator = this.dataset.operator;
		var id = this.dataset.cartid;
		console.log(operator, id);

		if (user == 'AnonymousUser')
		{	
					
			if (operator == 'plus')
			{
				increment(operator, id);
			}
		}
		else
		{
			if (operator == 'plus')
			{
				increment(operator, id);
			}
						
		}
		
	})
}

function increment(operator, id){

	let url = '/apicart/'

	fetch(url, {
		method : 'POST',
		headers : {
			'Content-Type' : 'application/json',
			'X-CSRFToken' : csrftoken,
		},
		body : JSON.stringify({'operator' : operator , 'id' : id})
	}).then(response => {
		return response.json()
	}).then(data => {
			console.log(data);	
			setTimeout(()=>{
             location.reload();
        	},2000)
	})
}



for ( let i = 0; i < minus.length; i+=1){
	minus[i].addEventListener('click', function(){
		var operator = this.dataset.operator;
		var id = this.dataset.cartid;
		console.log(operator, id);

		if (user == 'AnonymousUser')
		{	
					
			if (operator == 'minus')
			{
				decrement(operator, id);
			}
		}
		else
		{
			if (operator == 'minus')
			{
				decrement(operator, id);
			}
						
		}
		
	})
}

function decrement(operator, id){

	let url = '/apicart/'

	fetch(url, {
		method : 'POST',
		headers : {
			'Content-Type' : 'application/json',
			'X-CSRFToken' : csrftoken,
		},
		body : JSON.stringify({'operator' : operator , 'id' : id})
	}).then(response => {
		return response.json()
	}).then(data => {
			console.log(data);	
			setTimeout(()=>{
             location.reload();
        	},2000)
	})
}

