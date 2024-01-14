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

  let url = 'http://0.0.0.0:5001/api/v1/status/';
  $.get(url, function (data) {
    if (data.status === 'OK') {
      $('#api_status').addClass('available');
    } else {
      $('#api_status').removeClass('available');
    }
  });
});
