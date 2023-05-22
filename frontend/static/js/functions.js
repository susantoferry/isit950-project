let accMenuToggle = document.querySelector('.dropdown-menu-acc');
let dropdownToggle = document.querySelector('.dropdown-acc')
$(dropdownToggle).click(function () {
    console.log("a")
    accMenuToggle.classList.toggle('show')
})

function initMap() {

    var locations = [
        ['Bondi Beach', -33.890, 151.274, 4],
        ['Coogee Beach', -33.923, 151.259, 5],
        ['Cronulla Beach', -34.028, 151.157, 3],
        ['Manly Beach', -33.800, 151.287, 2],
        ['Maroubra Beach', -33.950, 151.259, 1]
      ];

    var options = {
        center: {lat: -34.407, lng: 150.878},
        zoom: 13,
        streetViewControl: false,
        mapTypeControl: false,
        fullscreenControl: false
    };

    map = new google.maps.Map(document.getElementById('map'), options);

    function addMarker(property) {
        const marker = new google.maps.Marker({
            position: property.location,
            map: map
        })

        const detailWindow = new google.maps.InfoWindow({
            content: property.content
        })

        marker.addListener("click", () => {
            detailWindow.open(map, marker)
        })
        
        google.maps.event.addListener(map, "click", function(event) {
            detailWindow.close();
        });
    }

    addMarker({location:{lat: -34.407, lng: 150.878}, content:`<h2>Test</h2>`})
    addMarker({location:{lat: -34.406, lng: 150.878}, content:`<h2>Test2</h2>`})
    addMarker({location:{lat: -34.393, lng: 150.894}, content:"<h2>Test3</h2>"})

    addMarker({location:{lat: -34.405, lng: 150.873}, content:`<h2>Test</h2>`})
    addMarker({location:{lat: -34.403, lng: 150.874}, content:`<h2>Test2</h2>`})
    addMarker({location:{lat: -34.395, lng: 150.890}, content:"<h2>Test3</h2>"})
    addMarker({location:{lat: -34.391, lng: 150.891}, content:"<h2>Test3</h2>"})
    addMarker({location:{lat: -34.390, lng: 150.899}, content:"<h2>Test3</h2>"})

    
}