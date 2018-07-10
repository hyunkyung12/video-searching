<?php
/**************************************************************************
 * MAIL UTILITY PHP SCRIPT
 * @author : NCodeArt
 * This file is licensed to NCodeArt (http://themeforest.net/user/ncodeart) and prohibited to copy or reuse it.
 * Copyright NCodeArt 2016
**************************************************************************/
require('php_wrappers/MailChimp.php');
require('php_wrappers/CMBase.php');
require('php_wrappers/GetResponseAPI.class.php');
require('config.php');

if($_SERVER["REQUEST_METHOD"] == "POST" && !empty($_POST["email"])) {

	if (isset($_POST["email"]["val"]) && is_array($_POST["email"])) {
		$email = $_POST["email"]["val"];
	} else {
		$email = $_POST["email"];
	}
	$firstname = isset($_POST["name"]["val"]) ? $_POST["name"]["val"] : '';
	
	header('HTTP/1.1 200 OK');
	header('Status: 200 OK');
	header('Content-type: application/json');

	// Checking if the email writing is good
	if(filter_var($email, FILTER_VALIDATE_EMAIL)) {
		
		/* The part for the storage in a .txt
		++++++++++++++++++++++++++++++++++++++++++++++*/
		if ($STORE_MODE == "file") {
			
			// SUCCESS SENDING
			if(@file_put_contents($STORE_FILE, strtolower($email)."\r\n", FILE_APPEND)) {
				echo json_encode(array(
					"status" => "success"
				));
			// ERROR SENDING
			} else {
				echo json_encode(array(
					"status" => "error",
					"type" => "FileAccessError"
				));
			}
		}

		/* MAILCHIMP
		++++++++++++++++++++++++++++++++++++++++++++++*/
		elseif ($STORE_MODE == "mailchimp") {
			
			$MailChimp = new \Drewm\MailChimp($MC_API_KEY);
			$result = $MailChimp->call('lists/subscribe', array(
						'id'                => $MC_LIST_ID,
						'email'             => array('email'=>$email, 'name'=>$firstname),
						'double_optin'      => false,
						'update_existing'   => true,
						'replace_interests' => false,
						'send_welcome'      => true,
					));     
	
			// SUCCESS SENDING
			if(isset($result["email"])) {
				if ($result["email"] == $email) {
					echo json_encode(array(
						"status" => "success"
					));
				}else{
					echo json_encode(array(
						"status" => "error",
						"type"   => "Looks like something went wrong. Please try again later."
					));
					errorlog("mailchimp", $result["name"]);
				}
			// ERROR SENDING
			} else {
				/*echo json_encode(array(
					"status" => "error",
					"type" => $result["name"]
				));*/
				echo json_encode(array(
					"status" => "error",
					"type"   => "Looks like something went wrong. Please try again later."
				));
				errorlog("mailchimp", $result["name"]);
			}
		}

		/* CAMPAIGN MONITOR
		++++++++++++++++++++++++++++++++++++++++++++++*/
		elseif ($STORE_MODE == "campaignmonitor") {
			$api_key     = $CM_API_KEY;
			$list_id     = $CM_LIST_ID;
			/*$client_id = null;
			$campaign_id = null;*/
			$cm          = new CampaignMonitor($api_key, null, null, $list_id);
			$result      = $cm->subscriberAdd($email, $firstname);
			
			// SUCCESS SENDING
			if($result['Result']['Code'] == 0) {     	
				echo json_encode(array(
					"status" => "success"
				));
				
			// ERROR SENDING
			} else {
				/*echo json_encode(array(
					"status" => "error",
					"type" => $result['Result']['Message']
				));*/
				echo json_encode(array(
					"status" => "error",
					"type"   => "Looks like something went wrong. Please try again later."
				));
				errorlog("campaignmonitor", "Error : ". $result['Result']['Code']." : ".$result['Result']['Message']);
			}
		}

		/* GET RESPONSE
		++++++++++++++++++++++++++++++++++++++++++++++*/
		elseif ($STORE_MODE == "getresponse") {
			$gr       = new GetResponse($GR_API_KEY);
			$campaign = $gr->getCampaignByName($GR_CAMPAIGN_NAME);
			$result   = $gr->addContact($campaign, $firstname, $email, 'standard', 0, array());

			// SUCCESS SENDING
			if(isset($result->queued) && $result->queued == 1) {
				echo json_encode(array(
					"status" => "success"
				));
				
			// ERROR SENDING
			} else {
				/*echo json_encode(array(
					"status" => "error",
					"type" => $result->message
				));*/
				echo json_encode(array(
					"status" => "error",
					"type"   => "Looks like something went wrong. Please try again later."
				));
				errorlog("getresponse", $result->message);
			}
		}

		/* ERROR
		++++++++++++++++++++++++++++++++++++++++++++++*/
		else {
			echo json_encode(array(
				"status" => "error",
				"type" => "Please select email storage type."
			));
		}
	// ERROR DURING THE VALIDATION 
	} else {
		echo json_encode(array(
			"status" => "error",
			"type" => "ValidationError"
		));
	}
} else {
	header('HTTP/1.1 403 Forbidden');
	header('Status: 403 Forbidden');
}

function errorlog($app, $details){

	$date = date("Y-m-d H:i:s");
	if (is_array($details)) {
		$info = '';
		foreach ($details as $key => $value) {
			$info .= $value."\n";
		}
	}else {
		$info = $details;
	}
	file_put_contents(
		"errorlog.txt", 
		$date." [".$app."]"."\n".
		$info."\n".
		"+++++++++++++++++++++++"."\n",
		FILE_APPEND
		);
}

?>