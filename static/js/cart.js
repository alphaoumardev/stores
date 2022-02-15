const updatebtn = document.getElementsByClassName('update-cart')
for(let i=0 ;i<updatebtn.length; i++)
{
    updatebtn[i].addEventListener('click', function()
    {
        let productId = this.dataset.product
		let action = this.dataset.action

        console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		if (user === 'AnonymousUser')
        {
			addCookieItem(productId, action)
            console.log("out")
		}
        else
        {
			updateItem(productId, action)
            console.log("in")

		}

    })
}
function addCookieItem(productId, action)
{
    console.log("The user is not authenticated")
    if(action === "add")
    {
        if(cart[productId] === undefined)
        {
            cart[productId]={"quantity":1}
        }else
        {
            cart[productId]["quantity"]+=1
        }
    }
    if(action === "remove")
    {
        cart[productId]["quantity"]-=1
        if(cart[productId]["quantity"] <= 0)
        {
            delete cart[productId]
        }
    }
    console.log("Cart:", cart)
    document.cookie = "cart="+JSON.stringify(cart)+";domain=;path=/"
}
function updateItem(productId, action)
{
    let url = "/update_item/"
     fetch(url,
        {
            method: "POST",
            headers: {"Content-Type": "application/json", 'X-CSRFToken':csrftoken},

            body: JSON.stringify({"productId": productId, "action": action})

        })
        .then((res) =>
        {
            let response = JSON.stringify(res);
            JSON.parse(response);
        })
}