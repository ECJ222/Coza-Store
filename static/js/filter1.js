//getting data from Html Elements

var filter = document.getElementsByClassName('filter');
console.log(filter);

for (let i = 0; i < filter.length; i+=1){
	filter[i].addEventListener('click', function(){
		var choice = this.dataset.filter;

		filterData(choice);
	})
}

//sending data to Django

function filterData(choice){

	let url = '/apifeature/'

	fetch(url, {
		method : 'POST',
		headers : {
			'Content-Type' : 'application/json',
			'X-CSRFToken' : csrftoken,
		},
		body : JSON.stringify({'choice' : choice})
	}).then( res => {
		return res.json()
	}).then( data => {
			console.log(data);	
			setTimeout(()=>{
             location.reload()
        	},4000)
	})
}

var click = document.getElementsByClassName('click')

for (let i = 0; i < click.length; i+=1){
		click[i].addEventListener('keypress', function(e){
			if (e.key === 'Enter')
			{
				submitData();
			}
		})
}

function submitData(){
	document.getElementById("Form").submit();
}
