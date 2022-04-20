var navbar_classes = "navbar-danger navbar-success navbar-warning navbar-dark navbar-light navbar-primary navbar-info navbar-pink";
$("#sidebar-dark-theme").on("click" , function(){
    document.body.classList.toggle("sidebar-dark");
    document.body.classList.toggle("dark-theme");
    if(document.body.classList.contains("sidebar-dark")){
      document.getElementById("sidebar-dark-theme").src = "images/sun.png";
      $(".navbar").removeClass(navbar_classes);
      $(".navbar").addClass("navbar-dark");
      $(".tiles").removeClass("selected");
      $(this).addClass("selected");
      localStorage.setItem("themeColor","dark-theme");
      document.getElementById("logo1").src = "images/logo-white.png";
    }else{
      document.getElementById("sidebar-dark-theme").src = "images/moon.png";
      $(".navbar").removeClass(navbar_classes);
      $(".tiles").removeClass("selected");
      $(this).addClass("selected");
      localStorage.setItem("themeColor","light-theme");
      document.getElementById("logo1").src = "images/logo.png";
    }
    
  });