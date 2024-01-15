$('document').ready(function () {
  let amenitiesList = {};
  $('input[type="checkbox"]').change(function () {
    if ($(this).is(':checked')) {
      amenitiesList[$(this).attr('data-id')] = $(this).attr('data-name');
    } else {
      delete amenitiesList[$(this).attr('data-id')];
    }

    let selectedAmenities = Object.values(amenitiesList)
    if (selectedAmenities.length === 0) {
      $('.amenities h4').html('&nbsp;');
    } else {
      $('.amenities h4').text(selectedAmenities.join(', '));
    }   
  });

  // Function to update the status
  function updateApiStatus() {
    $.get("http://127.0.0.1:5001/api/v1/status/", (data) => {
      if (data.status === "OK") {
        $("#api_status").addClass("available");
      } else {
        $("#api_status").removeClass("available");
      }
    }).fail(() => {
      $("#api_status").removeClass("available");
    });
  }

  // Initial status update
  updateApiStatus();
  setInterval(updateApiStatus, 30000);
});
