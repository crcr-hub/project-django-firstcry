
// Add to wishlist
$(document).ready(function() {
    $('.add-to-wishlist').on('click', function(event) {
        event.preventDefault();
        console.log("clicked")
        var productId = $(this).closest('.product').data('product-id');
        var size = $("#sizevalue").val();
        let this_val = $(this)
        console.log(this_val)
        var csrftoken = getCookie('csrftoken');
        console.log("this",productId);
        $.ajax({
          type: 'POST',
          url: '/add_to_wishlist/',
          data: {'product_id': productId,'size':size},
          dataType: 'json',
          headers: {'X-CSRFToken': csrftoken},
          success: function(response) {
            this_val.html("WISHLISTED")
            
              if (response.bool == true) {
                this_val.html("WISHLISTED")
                console.log("after",this_val);
                console.log("hiiiiii")
                console.log("Success! Data:");
                
           
                alert('Product added to wishlist!');
              } 
              else {
                  alert('Product already in wishlist.');
              }
          }
      });
      
    });

                    // Function to get CSRF token from cookies
                    function getCookie(name) {
                      var cookieValue = null;
                      if (document.cookie && document.cookie !== '') {
                          var cookies = document.cookie.split(';');
                          for (var i = 0; i < cookies.length; i++) {
                              var cookie = cookies[i].trim();
                              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                  break;
                              }
                          }
                      }
                      return cookieValue;
                    }

});

// remove from wishlist

$(document).ready(function() {
 

  $(document).on('click', '.remove-from-wishlist', function(event) {
  console.log(event)
  event.preventDefault();
    var productId = $(this).closest('.product').data('product-id');
    let this_val = $(this)
    console.log(productId)
    var csrftoken = getCookie('csrftoken');
    console.log("this",productId);
    $.ajax({
      type: 'POST',
      url: '/remove_from_wishlist',
      data: {'product_id': productId},
      dataType: 'json',
      headers: {'X-CSRFToken': csrftoken},
      success: function(response) {

        
          if (response.bool == true) {
            $(" .remove").load(location.href + " .remove")
            $(" #divid ").load(" # divid");
          } else {
              alert('Product already in wishlist.');
          }
      }
  });
  
  
});




  // Function to get CSRF token from cookies
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

});




// addto cart

$(document).ready(function() {
    $('.add-to-cart').on('click', function(event) {
        event.preventDefault();
        var productId = $(this).closest('.product').data('product-id');
        var size = $("#sizevalue").val();
        console.log("thish vaue ",size)
        let this_val = $(this)
        console.log(productId)
        var csrftoken = getCookie('csrftoken');
        console.log("this",productId);
        $.ajax({
          type: 'POST',
          url: '/add_to_cart',
          data: {'product_id': productId,'size':size},
          dataType: 'json',
          headers: {'X-CSRFToken': csrftoken},
          success: function(response) {
    
            this_val.html("ADDED TO CART")
            console.log(response)
              if (response.bool == true) {
                alert('Product added to cart!');
            
              } else {
                  alert('Product already in Cart.');
              }
          }
      });
      
    });
    
    
    
    
      // Function to get CSRF token from cookies
      function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
      }
    
    });
      
// size changer for one product with login

$(document).ready(function(){
  $(".size-changer").click(function(){ // click event to buttons with class 
      var buttonName = $(this).attr("name"); // Get the ID attribute of the clicked button
      var productId = $(this).data('product-id'); 
      var csrftoken = getCookie('csrftoken');
      console.log(buttonName)
      console.log(productId)
      $.ajax({
          type: 'POST',
          url: '/oneprod_filter',
          data: {'size': buttonName ,'pid':productId },
          dataType: 'json',
          headers: {'X-CSRFToken': csrftoken},
          success: function(res){
            
              console.log(res);
              $("#sizechange").html(res.data);
              // Handle success response if needed
          },
          error: function(xhr, status, error){
              console.error("Error sending button ID: ", error);
              // Handle error if needed
          }
      });
  });

  // Function to get CSRF token from cookies
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

});

