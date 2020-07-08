

//showWishlist
var wishlist = document.getElementsByClassName('js-show-cart1');
for (let i = 0; i < wishlist.length; i+=1){
	wishlist[i].addEventListener('click', function(){
		document.getElementById('panel').classList.add('show-header-cart');


	})
}
//showWishlist

//HideWishlist
var hidecart = document.getElementsByClassName('js-hide-cart1');
for (let i = 0; i < hidecart.length; i+=1){
	hidecart[i].addEventListener('click', function(){
		 document.getElementById('panel').classList.remove('show-header-cart');
	})
}
//HideCart

//Adding to Wishlist functionality

var unheart = document.getElementsByClassName('icon-heart2');
for (let i = 0; i < unheart.length; i+=1){
	unheart[i].addEventListener('click', function(){
		var productId = this.dataset.product;
		var action = this.dataset.action;

		console.log(productId,action)

		if( user == 'AnonymousUser'){
			Wishlist(productId,action);
		}
		else{
			Wishlist(productId,action);
		
		}
	})
}

//Adding to Wishlist functionality


console.log(unheart);
//Sending Data to Django

function Wishlist(productId,action){
	console.log(csrftoken);
	console.log('User is authenticated, sending data...')

	var url = '/api/'

	fetch(url, {
		method : 'POST',
		headers : {
			'Content-Type' : 'application/json',
			'X-CSRFToken' : csrftoken,
		},
		body : JSON.stringify({'productId':productId, 'action':action, 'user':user})
	})
	.then((response) => {

		return response.json()
		
	})
	.then((data) => {
			console.log(data);	
			setTimeout(()=>{
             location.reload()
        	},4000)
			
	});

}

//Sending Data to Django




/*
//remove wishlist data
var removewishlist = document.getElementsByClassName('header-cart-item-img');
for (let i = 0; i < removewishlist.length; i+=1)
{
	removewishlist[i].addEventListener('click', function(){
		var removeproduct = this.dataset.product;
		var removeaction = this.dataset.action;
		console.log(removeproduct, removeaction);

		if (user == 'AnonymousUser')
		{
			console.log(removeproduct, removeaction);
		}else
		{
			removefromwishlist(removeproduct, removeaction);
		}
	})
}
console.log(removewishlist);
//remove wishlist data

//send data to Django
console.log(csrftoken);
function removefromwishlist(removeproduct, removeaction){
	var url = 'http://127.0.0.1:8000/api/'

	fetch(url, {
		method : 'POST',
		headers : {
			'Content-Type' : 'application/json',
			'X-CSRFToken' : csrftoken,
			'Accept': 'application/json',
		},
		body : JSON.stringify({'productId':removeproduct, 'action':removeaction})
	})
	.then((response) => {
		return response.json()
	})
	.then((data) => {
			console.log(data);
			setTimeout(()=>{
             location.reload()
          },4000)
	});
}
//send data to Django*/