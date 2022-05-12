(function($) {
  'use strict';
  $(function() {
    $(".nav-settings").on("click", function() {
      $("#right-sidebar").toggleClass("open");
    });
    $(".settings-close").on("click", function() {
      $("#right-sidebar,#theme-settings").removeClass("open");
    });

    $("#settings-trigger").on("click" , function(){
      $("#theme-settings").toggleClass("open");
    });


    //background constants
    var navbar_classes = "navbar-danger navbar-success navbar-warning navbar-dark navbar-light navbar-primary navbar-info navbar-pink";
    var sidebar_classes = "sidebar-light sidebar-dark";
    var $body = $("body");

    // $(window).on('load', function () {
    //     var checkTheme = localStorage.getItem("themeColor");
    //     if(checkTheme === 'dark-theme'){
    //       document.body.classList.toggle("sidebar-dark");
    //       document.body.classList.toggle("dark-theme");
    //       document.getElementById("pager").classList.toggle("table-dark");
    //     }
    //     if(document.body.classList.contains("sidebar-dark")){
    //       document.getElementById("sidebar-dark-theme").src = "../static/assets/images/sun.png";
    //       $(".navbar").removeClass(navbar_classes);
    //       $(".navbar").addClass("navbar-dark");
    //       $(".tiles").removeClass("selected");
    //       $(this).addClass("selected");
    //       localStorage.setItem("themeColor","dark-theme");
    //       document.getElementById("logo1").style.display = "none";
    //       document.getElementById("logo2").style.display = "block";
    //     }else{
    //       document.getElementById("sidebar-dark-theme").src = "../static/assets/images/moon.png";
    //       $(".navbar").removeClass(navbar_classes);
    //       $(".tiles").removeClass("selected");
    //       $(this).addClass("selected");
    //       localStorage.setItem("themeColor","light-theme");
    //       document.getElementById("logo1").style.display = "block";
    //       document.getElementById("logo2").style.display = "none";
    //     }
    // });

    $("#sidebar-dark-theme").on("click" , function(){
      document.body.classList.toggle("sidebar-dark");
      document.body.classList.toggle("dark-theme");
      document.getElementById("pager").classList.toggle("table-dark");
      if(document.body.classList.contains("sidebar-dark")){
        document.getElementById("sidebar-dark-theme").src = "../static/assets/images/sun.png";
        $(".navbar").removeClass(navbar_classes);
        $(".navbar").addClass("navbar-dark");
        $(".tiles").removeClass("selected");
        $(this).addClass("selected");
        localStorage.setItem("themeColor","dark-theme");
        document.getElementById("logo1").src = "../static/assets/images/logo-white.png";
        // document.getElementById("logo2").style.display = "block";
      }else{
        document.getElementById("sidebar-dark-theme").src = "../static/assets/images/moon.png";
        $(".navbar").removeClass(navbar_classes);
        $(".tiles").removeClass("selected");
        $(this).addClass("selected");
        localStorage.setItem("themeColor","light-theme");
        document.getElementById("logo1").src = "../static/assets/images/logo.png";
        // document.getElementById("logo2").style.display = "none";
      }
      
    });


    //Navbar Backgrounds
    $(".tiles.primary").on("click" , function(){
      $(".navbar").removeClass(navbar_classes);
      $(".navbar").addClass("navbar-primary");
      $(".tiles").removeClass("selected");
      $(this).addClass("selected");
    });
    $(".tiles.success").on("click" , function(){
      $(".navbar").removeClass(navbar_classes);
      $(".navbar").addClass("navbar-success");
      $(".tiles").removeClass("selected");
      $(this).addClass("selected");
    });
    $(".tiles.warning").on("click" , function(){
      $(".navbar").removeClass(navbar_classes);
      $(".navbar").addClass("navbar-warning");
      $(".tiles").removeClass("selected");
      $(this).addClass("selected");
    });
    $(".tiles.danger").on("click" , function(){
      $(".navbar").removeClass(navbar_classes);
      $(".navbar").addClass("navbar-danger");
      $(".tiles").removeClass("selected");
      $(this).addClass("selected");
    });
    $(".tiles.light").on("click" , function(){
      $(".navbar").removeClass(navbar_classes);
      $(".navbar").addClass("navbar-light");
      $(".tiles").removeClass("selected");
      $(this).addClass("selected");
    });
    $(".tiles.info").on("click" , function(){
      $(".navbar").removeClass(navbar_classes);
      $(".navbar").addClass("navbar-info");
      $(".tiles").removeClass("selected");
      $(this).addClass("selected");
    });
    $(".tiles.dark").on("click" , function(){
      $(".navbar").removeClass(navbar_classes);
      $(".navbar").addClass("navbar-dark");
      $(".tiles").removeClass("selected");
      $(this).addClass("selected");
    });
    $(".tiles.default").on("click" , function(){
      $(".navbar").removeClass(navbar_classes);
      $(".tiles").removeClass("selected");
      $(this).addClass("selected");
    });
  });
})(jQuery);
