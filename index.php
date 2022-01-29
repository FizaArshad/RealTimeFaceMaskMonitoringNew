
<html>
<head>
  <title>Fetch image from database in PHP</title>
</head>
<body>

<h2>All Records</h2>

<table border="2">
  <tr>
    <td>Sr.No.</td>
    <td>Name</td>
    <td>Images</td>
  </tr>

<?php

include "dbConn.php"; // Using database connection file here

$records = mysqli_query($db,"select * from 2ndnotification"); // fetch data from database

while($data = mysqli_fetch_array($records))
{
?>
  <tr>
    
   <img src = "data:image/jpg;base64,' . base64_encode($row['rest']) . '" width = "50px" height = "50px"/>

    
  </tr>	
<?php
}
?>

</table>

<?php mysqli_close($db);  // close connection ?>

</body>
</html>
