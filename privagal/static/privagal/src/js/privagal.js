;(function ($) {

var $grid = $('.grid').packery({
  itemSelector: '.grid-item',
  columnWidth: '.grid-sizer',
  gutter: 0,
  percentPosition: true
});

// For the first time, wait for all images to be loaded before refreshing layout
$grid.imagesLoaded().done(function() {
  $grid.packery();
});

// Paginate list with ajax scroll instead.
$container = $('.grid-scroll');
if ($container.length) {

    var $ias = $.ias({
      container: '.grid-scroll',
      item: '.grid-item',
      pagination: '#pagination',
      next: '.next',
      delay: 1200
    });

    // See: http://infiniteajaxscroll.com/examples/masonry.html
    $ias.on('render', function(items) {
      $(items).css({ opacity: 0 });
    });
    $ias.on('rendered', function(items) {
      $grid
        .append(items)  // Append items in DOM with jQuery
        .packery('appended', items);  // Then trigger packery to refresh layout
    });

    $ias.extension(new IASSpinnerExtension());
    $ias.extension(new IASNoneLeftExtension({
        text: gettext("You reached the end!"),
        html: '<div class="ias-noneleft">' +
                '<div class="alert alert-warning" role="alert">' +
                    '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
                    '{text}' +
                '</div>' +
            '</div>'
    }));
}

// Initialize Bootstrap tooltip.
$('[data-toggle="tooltip"]').tooltip();

})(jQuery);
