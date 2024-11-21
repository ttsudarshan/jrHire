var stripe = Stripe(checkout_public_key);

const button = document.querySelector('button');

button.addEventListener('click' ,event =>{

    stripe.redirectToCheckout({
        sessionId: checkout_session
    }).then(function (result) {
        if (result.error) {
            alert(result.error.message);
        }
    });


})
