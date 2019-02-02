<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Home Page</title>
    <link rel="stylesheet" href="cate.css">
  </head>
  <body style="background-color:white;">
    <div class="dropdown">
      <button onclick="myFunction()" class="dropbtn">Categories</button>
      <div id="myDropdown" class="dropdown-content">
        <a href="cate1.php">Social Care</a>
        <a href="cate2.php">Animal Care</a>
        <a href="cate3.php">Development</a>
      </div>
    </div>
    <div class="upload">
        <a href="upload.html"><button type="button"  class="upl">Upload</button></a>
    </div>
    <div class="category3">
    </div>
    <script>
      function myFunction() {
        document.getElementById("myDropdown").classList.toggle("show");
      }
      // Close the dropdown menu if the user clicks outside of it
      window.onclick = function(event) {
          if (!event.target.matches('.dropbtn')) {
              var dropdowns = document.getElementsByClassName("dropdown-content");
              var i;
              for (i = 0; i < dropdowns.length; i++) {
                  var openDropdown = dropdowns[i];
                  if (openDropdown.classList.contains('show')) {
                    openDropdown.classList.remove('show');
                  }
              }
          }
      }
      //localStorage.clickcount = 0;
      //count = 0;
      function clickCounter(id_value) {
          /*if (typeof(Storage) !== "undefined") {
            if (localStorage.clickcount) {
              localStorage.clickcount = Number(localStorage.clickcount)+1;
            } else {
              localStorage.clickcount = 1;
          }*/
            //alert(id_value);
            count = 0;
            count++;
            var upvoteButton = document.getElementById(id_value);
            upvoteButton.innerHTML = "   "+ count + " Likes";
          }
    </script>
    <?php
        $dir = 'category3';
        $file_display = array('jpg', 'jpeg', 'png', 'gif');
        $dir_contents = scandir($dir);
        $count = 1;
        foreach ($dir_contents as $file){
            $file_type = explode(".",$file);
            if ( ($file !== '.' || $file !== '..') && in_array($file_type[1], $file_display) == true) {
                //echo $file ;
                echo '<img class = "images" src="category3/'.$file.'"/>' ;
                echo '<br>';
                echo '<button id = "upvote'.$count.'" onclick = "clickCounter(id)" >Upvote</button>' ;
                $count+=1;
                echo '<br>';echo '<br>';echo '<br>';
            }
        }
     ?>
   
  </body>
</html>
