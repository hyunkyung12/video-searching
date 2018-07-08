<?php
/**************************************************************************
 * MAIL UTILITY PHP SCRIPT
 * @author : NCodeArt
 * This file is licensed to NCodeArt (http://themeforest.net/user/ncodeart) and prohibited to copy or reuse it.
 * Copyright NCodeArt 2016
**************************************************************************/

/*
$STORE_MODE = "mailchimp";  		=> for Mail Chimp
$STORE_MODE = "campaignmonitor";	=> for Campaign Monitor
$STORE_MODE = "getresponse";		=> for GetResponse
$STORE_MODE = "file";				=> to save mail addresses in "subscription.txt" file.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
$STORE_MODE = "file";


/*
MAILCHIMP SETTINGS
---------------
Where can I find my API key? 
http://kb.mailchimp.com/accounts/management/about-api-keys
---------------
Where can I find my List ID?
http://kb.mailchimp.com/lists/managing-subscribers/find-your-list-id

MailChimp API Key findable in your Mailchimp's dashboard
MailChimp List ID  findable in your Mailchimp's dashboard
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
$MC_API_KEY =  "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";
$MC_LIST_ID =  "xxxxxxxxx";


/*
CAMPAIGN MONITOR SETTINGS
---------------
Where can I find my API key? 
http://help.campaignmonitor.com/topic.aspx?t=206
---------------
Where can I find my List ID?
https://www.campaignmonitor.com/api/getting-started/?&_ga=1.69755664.1469494041.1451461361#listid
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
$CM_API_KEY =  "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";
$CM_LIST_ID =  "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";


/*
GET RESPONSE SETTINGS
---------------
Where can I find my API key? 
http://apidocs.getresponse.com/pl/article/api-key
---------------
Campaign name as List ID
https://app.getresponse.com/campaign_list.html
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
$GR_API_KEY       =  "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";
$GR_CAMPAIGN_NAME =  "xxxxxxxxx";


/* TEXT FILE SETTINGS
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
// After $_SERVER["DOCUMENT_ROOT"]." , write the path to your .txt to save the emails of the subscribers
$STORE_FILE = "subscription.txt";
