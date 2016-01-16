window.onload = function() {
  var linkedName = window.location.hash.split('#')[1];

  var visUrl = "https://openaustin.cartodb.com/u/oa-admin/api/v2/viz/cb394812-8b56-11e5-91c0-0ecd1babdde5/viz.json"
  var toggleLayers = {};

  cartodb.createVis(map, visUrl)
    .on('done', function(vis, layers) {
      $.each(layers[1].layers, function(idx, layer) {
        var layerId = normalizeForCSS(layer.layer_name);
        toggleLayers[layerId] = layer;

        var element = $('<a>')
          .attr('id', layerId)
          .attr('href', '#' + layerId)
          .addClass('button')
          .addClass(layerId)
          .text(layer.layer_name)
          .click(function (event) {
            var clickedName = event.target.id;
            setLayer(clickedName);
          });

        $('#menu').prepend(element);

        if (linkedName && toggleLayers.hasOwnProperty(linkedName)) {
          setLayer(linkedName);
        } else if (idx === 0) {
          setLayer(layerId);
        }
      });
    });

  function setLayer(layerId) {
    $.each(toggleLayers, function(name, layer) {
      layer.sub.hide();
    });

    toggleLayers[layerId].sub.show();

    $('.button').removeClass('selected');
    $('#' + layerId).addClass('selected');
  }

  function normalizeForCSS(str) {
    return str.replace(/[^a-z0-9\ \-]/gmi, '').replace(/\ /g, '-')
  }
}
