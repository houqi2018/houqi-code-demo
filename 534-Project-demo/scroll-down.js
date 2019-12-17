$(document).ready(function(){
  $("a").on('click', function(event) {
    if (this.hash !== "") {
      event.preventDefault();
      var hash = this.hash;
      $('html, body').animate({
        scrollTop: $(hash).offset().top
      }, 800, function(){
        window.location.hash = hash;
      });
    } 
  });
});

$(document).ready(function() {
  $('.Question').click(function() {
    $('.Solution > div').removeClass('highlight');
    $('#' + $(this).data('color')).addClass("highlight");
  });
});