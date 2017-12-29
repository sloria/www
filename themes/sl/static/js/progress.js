(function() {
  var d = document;
  var p = d.getElementById('progress');
  function getScrollPercent() {
    return (window.pageYOffset / (d.body.scrollHeight - window.innerHeight)) * 100;
  }
  d.addEventListener("DOMContentLoaded", function() {
    p.style.width = getScrollPercent() + '%';
    window.addEventListener('scroll', function(e) {
      p.style.width = getScrollPercent() + '%';
    });
  });
})();
