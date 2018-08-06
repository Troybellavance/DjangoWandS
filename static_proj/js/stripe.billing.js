$(document).ready(function(){

  var stripeFormModule = $(".stripe-payment-form")
  var stripeModuleBtnTitle = stripeFormModule.attr("data-btn-title")
  var stripeModuleNextUrl = stripeFormModule.attr("data-next-url")
  var stripeModuleToken = stripeFormModule.attr("data-token")
  var stripeTemplate = $.templates("#stripeTemplate")
  var stripeTemplateContext = {
     btnTitle: stripeModuleBtnTitle,
     nextUrl: stripeModuleNextUrl,
     publishKey: stripeModuleToken
  }
  var stripeTemplateHtml = stripeTemplate.render(stripeTemplateContext)
  stripeFormModule.html(stripeTemplateHtml)


  var paymentForm = $(".payment-form")

  if (paymentForm.length > 1){
      alert("One payment form only per page.")
      paymentForm.css('display', 'none')
  }
  else if (paymentForm.length == 1){

  var nextUrl = paymentForm.attr('data-next-url')
  var publicKey = paymentForm.attr('data-token')

  // Create a Stripe client.
  var stripe = Stripe(publicKey);

  // Create an instance of Elements.
  var elements = stripe.elements();

  // Custom styling can be passed to options when creating an Element.
  // (Note that this demo uses a wider set of styles than the guide below.)
  var style = {
    base: {
      color: '#32325d',
      lineHeight: '18px',
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: 'antialiased',
      fontSize: '16px',
      '::placeholder': {
        color: '#aab7c4'
      }
    },
    invalid: {
      color: '#fa755a',
      iconColor: '#fa755a'
    }
  };

  // Create an instance of the card Element.
  var card = elements.create('card', {style: style});

  // Add an instance of the card Element into the `card-element` <div>.
  card.mount('#card-element');

  // Handle real-time validation errors from the card Element.
  card.addEventListener('change', function(event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
      displayError.textContent = event.error.message;
    } else {
      displayError.textContent = '';
    }
  });


  // Handle form submission
  // var form = document.getElementById('payment-form');
  // form.addEventListener('submit', function(event) {
  //   event.preventDefault();
  //
  //   var loadTime = 1500
  //   var errorHtml = "<i class='fa fa-warning'></i> An error has occured."
  //   var errorClasses = "btn btn-warning disabled my-2"
  //   var loadingHtml = "<i class='fa fa-spin fa-spinner'></i> Loading..."
  //   var loadingClasses = "btn btn-primary disabled my-2"
  //
  //   stripe.createToken(card).then(function(result) {
  //     if (result.error) {
  //       // Inform the user if there was an error
  //       var errorElement = document.getElementById('card-errors');
  //       errorElement.textContent = result.error.message;
  //     } else {
  //       // Send the token to your server
  //       stripeTokenHandler(nextUrl, result.token);
  //     }
  //   });
  // });

  // Same as above but converted for jQuery use
  var form = $('#payment-form');       // if class instead ('.payment-form') var $this = $(this) & $this.find('.btn-load')
  form.on('submit', function(event) {  //this for now as it's more reusable
    event.preventDefault();

    var btnLoad = form.find('.btn-load')
    var loadTime = 1500
    var currentTimeout;
    var errorHtml = "<i class='fa fa-warning'></i> An error has occured."
    var errorClasses = "btn btn-warning disabled my-2"
    var loadingHtml = "<i class='fa fa-spin fa-spinner'></i> Loading..."
    var loadingClasses = "btn btn-primary disabled my-2"

    stripe.createToken(card).then(function(result) {
      if (result.error) {
        // Inform the user if there was an error
        var errorElement = $('#card-errors');
        errorElement.textContent = result.error.message;
      } else {
        // Send the token to your server
        stripeTokenHandler(nextUrl, result.token);
      }
    });
  });

  function displayStatusBtn(element, newHtml, newClasses, loadTime, timeout){
    if (timeout){
      clearTimeout(timeout)
    }
      var defaultHtml = element.html()
      var defaultClasses = element.attr("class")
      element.html(newHtml)
      element.removeClass(defaultClasses)
      element.addClass(newClasses)
      return setTimeout(function(){
          element.html(defaultHtml)
          element.addClass(defaultClasses)
          element.removeClass(newClasses)
      }, loadTime)
  }

  function redirectToNext(nextPath, timeoffset) {
      if (nextPath){
      setTimeout(function(){
                  window.location.href = nextPath
              }, timeoffset)
      }
  }
  function stripeTokenHandler(nextUrl, token){
      var paymentMethodEndpoint = '/billing/payment-method/create/'
      var data = {
          'token': token.id
      }
      $.ajax({
          data: data,
          url: paymentMethodEndpoint,
          method: "POST",
          success: function(data){
              var succesMsg = data.message || "Card was successfully added."
              card.clear()
              if (nextUrl){
                  succesMsg = succesMsg + "<br/><br/><i class='fa fa-spin fa-spinner'></i> Redirecting..."
              }
              if ($.alert){
                  $.alert(succesMsg)
              } else {
                  alert(succesMsg)
              }
              redirectToNext(nextUrl, 2000)

          },
          error: function(error){
              console.log(error)
        }
      })
  }
  }
})
