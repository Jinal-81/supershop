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
                $("body").removeAttr("style");
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
            <div class="addressAddress_type" name="address_type">${address.address_type}</div>
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
        console.log('#################')
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
            $('.modal-backdrop').hide();// hide modal
            $(this).hide();
            $("body").removeAttr("style"); // remove style overflow from the body tag
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
//    debugger;
    if(data.deleted) // data delete true of false
    {
//        debugger;
        $("#userTable #address-" + data.id).remove(); // remove record by id
        $("#myModaldelete").toggle();
        $('.modal-backdrop').hide();
        $(this).hide();
        $("body").removeAttr("style"); // remove style overflow from the body tag
//        (data.address);
//            $("#myModal").modal("hide");
        $('.modal-backdrop').remove();
        $("#myModaldelete").modal("hide");
        $(this).hide();
        $("body").removeAttr("style"); // remove style overflow from the body tag
        window.location.reload();
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
$('.card-header').click(function() {
            $(this).find('i').toggleClass('bi bi-chevron-double-up');
});