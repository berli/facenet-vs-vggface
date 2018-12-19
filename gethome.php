<?php 
    // create curl resource 
   $ch = curl_init(); 

   // set url 
   curl_setopt($ch, CURLOPT_URL, "https://github.com/search?q=react"); 

   //return the transfer as a string 
   curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 

   // $output contains the output string 
   $output = curl_exec($ch); 

    //echo output
    echo $output;

   // close curl resource to free up system resources 
   curl_close($ch);      
?>
