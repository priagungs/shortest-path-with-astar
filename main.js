function initITB(){
    var loc = {lat: -6.891192, lng: 107.610627};
    initMap(loc);
}

function initAlun(){
    var loc = {lat: -6.921749, lng: 107.607081};
    initMap(loc);
}

function initMap(loc) {
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 15,
      center: loc
    });
    var marker = new google.maps.Marker({
      position: loc,
      map: map
    });
  }
