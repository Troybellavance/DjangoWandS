$(document).ready(function(){
  // Contact form handling

  var contactForm = $(".contact-form")
  var contactFormMethod = contactForm.attr("method")
  var contactFormEndpoint = contactForm.attr("action")


  function displaySubmission(submitButton, defaultText, doSubmitting){

    if (doSubmitting){
      submitButton.addClass("disabled")
      submitButton.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
    } else {
      submitButton.removeClass("disabled")
      submitButton.html(defaultText)
    }

  }

  contactForm.submit(function(event){
    event.preventDefault()
    
    var contactFormButton = contactForm.find("[type='submit']")
    var contactFormButtonText = contactFormButton.text()
    var contactFormData = contactForm.serialize()
    var thisForm = $(this)
    displaySubmission(contactFormButton, "", true)
    $.ajax({
      method: contactFormMethod,
      url: contactFormEndpoint,
      data: contactFormData,
      success: function(data){
        contactForm[0].reset()
        $.alert({
          title: "Success!",
          content: data.message,
          theme: "dark",
        })
        setTimeout(function(){
          displaySubmission(contactFormButton, contactFormButtonText, false)
        }, 750)
      },
      error: function(error){
        console.log(error.responseJSON)
        var jsonData = error.responseJSON
        var msg = ""

        $.each(jsonData, function(key, value){
          msg += key + ": " + value[0].message + "<br/>"
        })
        $.alert({
          title: "Oops!",
          content: msg,
          theme: "dark",
        })

        setTimeout(function(){
          displaySubmission(contactFormButton, contactFormButtonText, false)
        }, 750)
      }
    })
  })


  //auto-search

   var searchForm = $(".search-form")
   var searchInput = searchForm.find("[name='q']")
   var typingTimer;
   var typingInterval = 1250
   var searchButton = searchForm.find("[type='submit']")

   searchInput.keyup(function(event){
      clearTimeout(typingTimer)
      typingTimer = setTimeout(performSearch, typingInterval)
   })

   searchInput.keydown(function(event){
      clearTimeout(typingTimer)
   })

   function activeSearchDisplay(){
     searchButton.addClass("disabled")
     searchButton.html("<i class='fa fa-spin fa-spinner'></i> Searching...")
   }

   function performSearch(){
     activeSearchDisplay()
     var query = searchInput.val()
     setTimeout(function(){
       window.location.href='/search/?q=' + query
     }, 1000)

   }

  //Cart & Products

  var productForm = $(".product-form-ajax") //form-product-ajax

  productForm.submit(function(event){
      event.preventDefault();
      var thisForm = $(this)
      //var actionEndpoint = thisForm.attr("action"); //Could be done this way to prevent breaking on javascript disabled/incapable browsers.
      var actionEndpoint = thisForm.attr("endpoint")
      var httpMethod = thisForm.attr("method");
      var formData = thisForm.serialize();

      $.ajax({
        url: actionEndpoint,
        method: httpMethod,
        data: formData,
        success: function(data){
          var submitSpan = thisForm.find(".submit-span")
          if (data.added){
            submitSpan.html("Item in cart <button type='submit' class='btn btn-link'> Remove Item </button>")
          } else {
            submitSpan.html("<button type='submit' class='btn btn-success'> Add to cart </button>")
          }
          var navbarCount = $(".navbar-count-in-cart")
          navbarCount.text(data.cartItemCount)
          var currentPath = window.location.href

          if (currentPath.indexOf("cart") != -1){
            refreshCart()
          }
        },
        error: function(errorData){
          $.alert({
            title: "Oops!",
            content: "An unexpected error has occurred.",
            theme: "dark",
          })

        }
      })
    })

    function refreshCart(){
      console.log("in current cart")
      var cartTable = $(".cart-table")
      var cartBody = cartTable.find(".cart-body")
      //cartBody.html("<h3>Cart Changed</h3>")
      var productRows = cartBody.find(".cart-product")
      var currentUrl = window.location.href

      var refreshCartUrl = '/api/cart/';
      var refreshCartMethod = "GET";
      var data ={};
      $.ajax({
        url: refreshCartUrl,
        method: refreshCartMethod,
        data: data,
        success: function(data){

          var hiddenCartItemRemovalForm =  $(".cart-item-removal-form")
          if (data.products.length > 0){
            productRows.html(" ")
            i = data.products.length
            $.each(data.products, function(index, value){
              var newCartItemRemoval = hiddenCartItemRemovalForm.clone()
              newCartItemRemoval.css("display", "block")
              //newCartItemRemoval.removeClass("hidden-class")
              newCartItemRemoval.find(".cart-product-id").val(value.id)
                cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value
                .name + "</a>" + newCartItemRemoval.html() + "</td><td>" + value.price + "</td></tr>")
              i --
            })
            cartBody.find(".cart-subtotal").text(data.subtotal)
            cartBody.find(".cart-total").text(data.total)
          } else {
            window.location.href = currentUrl
          }
        },
        error: function(errorData){
          $.alert({
            title: "Oops!",
            content: "An unexpected error has occurred.",
            theme: "dark",
          })
        }
      })
    }
  })
