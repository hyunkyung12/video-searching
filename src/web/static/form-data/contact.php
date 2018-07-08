<?php
if ($_POST['formtype'] == 'table-booking') {
	$name          = $_POST['name'];
	$email_address = $_POST['email'];
	$phone         = $_POST['phone'];
	$date          = $_POST['date'];
	$people        = $_POST['people'];
	
	echo $name;
	echo $email_address;
	echo $phone;
	echo $date;
	echo $people;
	$to            = 'jayesh.kava007@gmail.com'; //Just write your email
	$email_subject = "Booking form submitted by:  $name";
	$email_body    = "You have received a new message. <br/>".
				  	 "Here are the details: <br/><br/> Name: $name <br/><br/>".
			         "Email: $email_address <br/><br/> Phone: $phone <br/><br/> Date: $date <br/><br/> No. of people: $people";
	$headers = "From:<$email_address>\n";
	$headers.= "Content-Type:text/html; charset=UTF-8";
	if($email_address != "") {
		mail($to,$email_subject,$email_body,$headers);
		return true;
	}

} elseif ($_POST['formtype'] == 'appointment') {
	$name          = $_POST['name'];
	$email_address = $_POST['email'];
	$phone         = $_POST['phone'];
	$treatment     = $_POST['treatment'];
	
	echo $name;
	echo $email_address;
	echo $phone;
	echo $treatment;
	$to            = 'jayesh.kava007@gmail.com'; //Just write your email
	$email_subject = "Appointment form submitted by:  $name";
	$email_body    = "You have received a new message. <br/>".
				  	 "Here are the details: <br/><br/> Name: $name <br/><br/>".
			         "Email: $email_address <br/><br/> Phone: $phone <br/><br/> Treatment: $treatment";
	$headers = "From:<$email_address>\n";
	$headers.= "Content-Type:text/html; charset=UTF-8";
	if($email_address != "") {
		mail($to,$email_subject,$email_body,$headers);
		return true;
	}

} else {
	$name          = $_POST['name'];
	$email_address = $_POST['email'];
	$message       = $_POST['message'];

	echo $name;
	echo $email_address;
	echo $message;
	$to = 'jayesh.kava007@gmail.com'; //Just write your email
	$email_subject = "Contact form submitted by:  $name";
	$email_body = "You have received a new message. <br/>".
				  "Here are the details: <br/><br/> Name: $name <br/><br/>".
			      "Email: $email_address <br/><br/> Message: <br/> $message";
	$headers="From:<$email_address>\n";
	$headers.="Content-Type:text/html; charset=UTF-8";
	if($email_address != "") {
		mail($to,$email_subject,$email_body,$headers);
		return true;
	}
}	


?>