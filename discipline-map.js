window.onload = function() {
  var linkedName = window.location.hash.split('#')[1];

  var visUrl = "https://openaustin.cartodb.com/u/oa-admin/api/v2/viz/cb394812-8b56-11e5-91c0-0ecd1babdde5/viz.json"
  var toggleLayers = {};

  cartodb.createVis(map, visUrl)
    .on('done', function(vis, layers) {
      for (var i = 0, len = layers[1].layers.length; i < len; i++) {
        layer = layers[1].layers[i];
        toggleLayers[layer.layer_name] = layer;

        var element = $('<a>')
          .attr('id', layer.layer_name)
          .attr('href', '#' + layer.layer_name)
          .addClass('button')
          .addClass(layer.layer_name)
          .text(layer.layer_name)
          .click(function (event) {
            var clickedName = event.target.id;
            setLayer(clickedName);
          });
        $('#menu').prepend(element);

        if (linkedName !== '' && toggleLayers.hasOwnProperty(linkedName)) {
          setLayer(linkedName);
        } else if (i === 0) {
          setLayer(layer.layer_name);
        }
      };
    });

  function setLayer(layerName) {
    Object.keys(toggleLayers).forEach(function(key) {
      toggleLayers[key].sub.hide();
    })

    toggleLayers[layerName].sub.show();

    $('.button').removeClass('selected');
    $('#' + layerName).addClass('selected');
  }
}
