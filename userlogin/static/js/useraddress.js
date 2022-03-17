// function for collapse
$(document).ready(function(){
    $(".addressData").on("click", function(){
        $(".collapse.show").collapse("toggle")
        $(this).parent().parent().parent().children(".collapse").collapse("toggle")
    })
})
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
// function for fields value
function trimValue(element){
    return $(element).val().trim()
}
// function for save data
$("#btnsave").click(function () {
    console.log("save button clicked")
    var cityInput = trimValue(CityElement)
    var landmarkInput = trimValue(LandmarkElement)
    var zipcodeInput = trimValue(ZipcodeElement)
    var stateInput = trimValue(StateElement)
    var address_typeInput = trimValue(AddressTypeElement)
    //check that fields are not empty or valid fields
    if (cityInput && landmarkInput && zipcodeInput && stateInput && address_typeInput) {
        // Create Ajax Call
        $.ajax({
            url: '/address/',
            type: 'POST',
            data: {
                'city': cityInput,
                'landmark': landmarkInput,
                'zipcode': zipcodeInput,
                'state': stateInput,
                'address_type': address_typeInput
            },
            dataType: 'json',
            success: function (data) {
                if (data.address) {
                  appendToUsrTable(data.address);
                  $("form")[0].reset(); // reset all the fields as blank
                  window.location.reload(true);
                }
            }
        });
    return false;

});
// update data into table
function appendToUsrTable(address) {
    console.log("table data")
    console.log(address)
      $("#userTable").append(`
    <div id="address-${address.id}" class="card">
      <div class="card-header">
        <a class="btn" aria-expanded="false" data-bs-toggle="collapse" data-bs-target="#panel-box"">
            <div class="addressAddress_type">${address.address_type}</div>
        </a>
      </div>
      <div id="panel-box" class="collapse">
        <div class="card-body">
            <div class="addressCity addressData">${address.city}</div><div class="addressLandmark addressData">${address.landmark}</div><div class="addressZipcode addressData" >${address.zipcode}</div><div class="addressState addressData">${address.state}</div>
            <button class="btn btn-success btn-edit" onClick="editAddress(${address.id})" data-bs-toggle="modal" data-bs-target="#myModal"><i class="bi bi-pencil-square"></i></button>
            <button class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="bi bi-trash-fill"></i></button>
//            <button class="btn btn-danger btn-del" onClick="deleteAddress(${address.id})" data-bs-toggle="modal"><i class="bi bi-trash-fill"></i></button>
        </div>
      </div>
    </div>
   </div>
    `);
}

// Create Django Ajax Call update the data
$("form#updateAddress").submit(function() {
    console.log('updated Clicked')
    var idInput = trimValue(IDFormElement)
    var cityInput = trimValue(CityFormElement)
    var landmarkInput = trimValue(LandmarkFormElement)
    var zipcodeInput = trimValue(ZipcodeFormElement)
    var stateInput = trimValue(StateFormElement)
    var address_typeInput = trimValue(AddressTypeFormElement)
    if (idInput && cityInput && landmarkInput && zipcodeInput && stateInput && address_typeInput) {
        // Create Ajax Call
        $.ajax({
            url: '/user_address_update/',
            type: 'POST',
            data: {
                'id': idInput,
                'city': cityInput,
                'landmark': landmarkInput,
                'zipcode': zipcodeInput,
                'state': stateInput,
                'address_type': address_typeInput
            },
            dataType: 'json',
            success: function (data) {
                if (data.address) {
                    console.log("call table after update")
                    updateToUserTabel(data.address);
                   }
            }
        });
        }
    $('form#updateUser').trigger("reset");
    $('#myModal').modal('hide');
    return false;
});

// Update Django Ajax Call this is for updating form by id
function editAddress(id) {
    console.log('edit clicked')
  if (id) {
    div_id = "#address-" + id; //# is important
    console.log(div_id)
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
  console.log("after if statement")
}
// check one by one filed name and update data accordingly into table.
function updateToUserTabel(address){
    console.log('user updated table')
    $("#userTable #address-" + address.id).children(".addressData").each(function()
    {
        var attr = $(this).attr("name"); // attribute for the field
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
//    debugger;
//  var action = confirm("Are you sure you want to delete this Address?");
//  if (action != false) {
    $.ajax({
        url: '/remove_address/',
        type: 'POST',
        data: {
            'id': id,
        },
        dataType: 'json',
        success: function (data) {
            if (data.deleted) {
              $("#userTable #address-" + id).remove();
            }
        }
    });
//  }
}

$(function() {
  // Initialize form validation on the registration form.
  // It has the name attribute "registration"
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
      city: "Please enter your City name",
      landmark: "Please enter your near by landmark",
      zipcode: "Please enter valid zipcode",
      state: "Please enter valid state",
      address_type: "Please enter valid address_type"
    },
    // Make sure the form is submitted to the destination defined
    // in the "action" attribute of the form when valid
//    submitHandler: function(form) {
//      form.submit();
//    }
  });
});

