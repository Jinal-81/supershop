// function for collapse
$(document).ready(function(){
    $(".addressData").on("click", function(){
        $(".collapse.show").collapse("toggle")
        $(this).parent().parent().parent().children(".collapse").collapse("toggle")
    })

})

// ajax function
function ajaxcall(url, data){
    var ajaxResponse = $.ajax({
        type: "POST",
        url: url,
        data: data,
    });

    return ajaxResponse
}
// variables
var CityElement = 'input[name="city"]'
var LandmarkElement = 'input[name="landmark"]'
var ZipcodeElement = 'input[name="zipcode"]'
var StateElement = 'input[name="state"]'
var AddressTypeElement = 'input[name="address_type"]'
var IDFormElement = 'input[name="formId"]'
var CityFormElement = 'input[name="formCity"]'
var LandmarkFormElement = 'input[name="formLandmark"]'
var ZipcodeFormElement = 'input[name="formZipcode"]'
var StateFormElement = 'input[name="formState"]'
var AddressTypeFormElement = 'input[name="formAddress_type"]'
var IDDeleteFormElement = 'input[name="formdeleteId"]'
var QuantityElement = 'input[name="quantity"]'

//function for elements
function trimValue(element){
    return $(element).val().trim()
}

// address create ajax call
$("form#addAddress").submit(function() {
    //here id is addAddress and if button is submit type then it will execute
    var cityInput = trimValue(CityElement)
    var landmarkInput = trimValue(LandmarkElement)
    var zipcodeInput = trimValue(ZipcodeElement)
    var stateInput = trimValue(StateElement)
    var address_typeInput = trimValue(AddressTypeElement)
    //check that fields are not empty or valid fields
    if (cityInput && landmarkInput && zipcodeInput && stateInput && address_typeInput) {
        // Create Ajax Call
        var data = { //data for the fields ( data that we want to send)
                'city': cityInput,
                'landmark': landmarkInput,
                'zipcode': zipcodeInput,
                'state': stateInput,
                'address_type': address_typeInput
            }
            ajaxcall('/address/', data).then(function(data){
            if(data.address){
                appendToUsrTable(data.address); // call html for data save
                $("#exampleModal").toggle();
                $('.modal-backdrop').hide();// hide modal
                $(this).hide();
                $("#bodyid").css({"overflow":"overlay"});//set new style
            }
        })
        $("form")[0].reset(); // reset all the fields as blank
    }
    return false;
});
// update data into table
function appendToUsrTable(address) {
  // data append to the html page
  $("#userTable").append(`
    <div id="address-${address.id}" class="card mt-3 p-sm-1">
      <div class="card-header">
        <a class="btn" aria-expanded="false" data-bs-toggle="collapse" data-bs-target="#panel-box"">
            <div class="addressAddress_type" name="address_type">${address.address_type}<i class="bi bi-chevron-double-down" id="arrowmargin"></i></div>
        </a>
      </div>
      <div id="panel-box" class="collapse show">
        <div class="card-body">
            <div class="addressCity addressData" name="city">${address.city}</div>
            <div class="addressLandmark addressData" name="landmark">${address.landmark}</div>
            <div class="addressZipcode addressData" name="zipcode">${address.zipcode}</div>
            <div class="addressState addressData" name="state">${address.state}</div>
             <button class="btn btn-success" onClick="editAddress(${address.id})" data-bs-toggle="modal" data-bs-target="#myModal"><i class="bi bi-pencil-square"></i></button>
             <button class="btn btn-danger" onClick="deleteAddress(${address.id})" data-bs-toggle="modal"><i class="bi bi-trash-fill"></i></button>
        </div>
      </div>
    </div>
    `);
}
// Create Django Ajax Call update the data
$("form#updateAddress").submit(function(e) {
    e.preventDefault();

    var form = $(this);

    var idInput = trimValue(IDFormElement)
    var cityInput = trimValue(CityFormElement)
    var landmarkInput = trimValue(LandmarkFormElement)
    var zipcodeInput = trimValue(ZipcodeFormElement)
    var stateInput = trimValue(StateFormElement)
    var address_typeInput = trimValue(AddressTypeFormElement)
    if (cityInput && landmarkInput && zipcodeInput && stateInput && address_typeInput) {
        // Create Ajax Call
        var data = { //data for the fields ( data that we want to send)
                'id': idInput,
                'city': cityInput,
                'landmark': landmarkInput,
                'zipcode': zipcodeInput,
                'state': stateInput,
                'address_type': address_typeInput
            }
        // call custom ajax function
        ajaxcall('/user_address_update/',data).then(function(data){
        if(data.address){
            updateToUserTabel(data.address); // call html page after update
            $("#myModal").toggle();
//            $(this).hide();
            $('.modal-backdrop').remove();// hide modal
//            $("#divid").load(" #divid");
            $("#bodyid").css({"overflow":"overlay"});//set new style
            }
        });
    }
    $('form#updateAddress').trigger("reset"); // reset fields after update
    return false;
});

// Update Django Ajax Call this is for updating form by id
function editAddress(id) {
  // if id exists then update data accordingly
  if (id) {
    div_id = "#address-" + id; //# is important
    city = $(div_id).find(".addressCity").text();
    landmark = $(div_id).find(".addressLandmark").text();
    zipcode = $(div_id).find(".addressZipcode").text();
    state = $(div_id).find(".addressState").text();
    address_type = $(div_id).find(".addressAddress_type").text();
    $('#form-id').val(id);
    $('#form-city').val(city);
    $('#form-landmark').val(landmark);
    $('#form-zipcode').val(zipcode);
    $('#form-state').val(state);
    $('#form-address_type').val(address_type);
  }
}
// check one by one filed name and update data accordingly into table.
function updateToUserTabel(address){
    $("#userTable #address-" + address.id).children().find(".addressData").each(function()
    {
        // attribute for the field
        var attr = $(this).attr("name");
        if (attr == "id") {
            $(this).text(address.id)
        } else if (attr == "city") {
          $(this).text(address.city);
        } else if (attr == "landmark") {
          $(this).text(address.landmark);
        } else if (attr == "zipcode") {
          $(this).text(address.zipcode);
        } else if (attr == "state") {
          $(this).text(address.state);
        } else {
          $(this).text(address.address_type);
        }
      });
}

// Delete Django Ajax Call
function deleteAddress(id) {
    // if id exists then delete data
    if (id) {
    div_id = "#address-" + id; //# is important
    $('#form-iddelete').val(id);
  }
}
// Create Django Ajax Call delete the data
$("form#deleteAddress").submit(function(e) {
    console.log('delete')
    e.preventDefault();

    var form = $(this);

    var idInput = trimValue(IDDeleteFormElement) // fetch id
    var data = { //data for the fields ( data that we want to send)
            'id': idInput
        }
    ajaxcall('/remove_address/',data).then(function(data){
    if(data.deleted) // data delete true of false
    {
        $("#userTable #address-" + data.id).remove(); // remove record by id
        $("#myModaldelete").toggle();
        $('.modal-backdrop').hide();
//        $(this).hide();
        $("#bodyid").css({"overflow":"overlay"});//set new style
        }
    });
    return false;
});

// validation function
$(function() {
  // Initialize form validation on the registration form.
  // It has the name attribute "addressadd"
  $("form[name='addressadd']").validate({
    // Specify validation rules
    rules: {
      // The key name on the left side is the name attribute
      // of an input field. Validation rules are defined
      // on the right side
      city: "required",
      landmark: "required",
      zipcode: "required",
      state: "required",
      address_type: "required"
    },
    // Specify validation error messages
    messages: {
      city: "<div class='errormessage'>Please enter your City name</div>",
      landmark: "Please enter your near by landmark",
      zipcode: "Please enter valid zipcode",
      state: "Please enter valid state",
      address_type: "Please enter valid address_type"
    },
  });
});
// arrow up down for collapse
$('.addressData').click(function() {
            $(this).find('i').toggleClass('bi bi-chevron-double-up');
});
// quantity change for products
$( "div input[type='number']" ).on('change',function() {
   const message = document.querySelector('#message1')
   console.log(message);
   const total = document.querySelector('.total')
   console.log(total);
   var quantityId = $(this).closest('.product_data').find('.prod_id').val();
   console.log(quantityId)
   var quantityVal = $(this).closest('.product_data').find('.quantityData').val();
   var total_amount = $('.total').text();
   console.log(total_amount)
   var quantity = $(this).val();
   console.log('quantity for click',quantity)
   var data = { //data for the fields ( data that we want to send)
                'id': quantityId,
                'quantity': quantityVal,
                'total_amount': total_amount
            }
        // call custom ajax function
        var url = "/cart/cartitem_update/" + quantityId;
        $.ajax({
            url: url,
            method: 'POST',
            data: {id: quantityId, quantity: quantity, total_amount: total_amount},
            cache: false,
            dataType: 'html',
            success: function(quantity_response) {
                console.log('success');
                data = JSON.parse(quantity_response); // response we are getting string , so convert it into json format
                console.log(data);
                console.log(data["total_amount"]);
                if(data["status"] == 'success')
                {
                   $("#message1").css({"display":"contents"});
                   message.innerHTML = `<div class="alert alert-dismissible alert-success fade show shadow">
                                          <strong>${data["message"]}</strong>
                                          <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                                        </div>`;
                   total.innerHTML = `&#8377;${data["total_amount"]} `;
                }
                else if(data["status"] == 'error')
                {
                    $("#message1").css({"display":"contents"});
                    message.innerHTML = `<div class="alert alert-dismissible alert-danger fade show shadow">
                                              <strong>${data["message"]}</strong>
                                              <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                                            </div>`
                }
            },
        });
     });
