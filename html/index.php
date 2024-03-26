<?php
$host = 'db';
$user = 'user';
$password = 'password';
$db = 'mydatabase';

$conn = new mysqli($host, $user, $password, $db);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT userid, username FROM users";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        echo "User ID: " . $row["userid"]. " - Name: " . $row["username"]. "<br>";
    }
} else {
    echo "0 results";
}
$conn->close();
?>
