<?php

	if (!empty($argv[1])) {
		parse_str($argv[1], $_GET);
	}

	function get_get ($name) {
		if(array_key_exists($name, $_GET)) {
			return $_GET[$name];
		} else {
			return NULL;
		}
	}

	$listings = "listings.csv";

	$pw_file = "/etc/ekz_pw_file";
	if(file_exists($pw_file)) {
		$pw = file_get_contents($pw_file);
		$pw = rtrim($pw);
		$arg_pw = get_get("pw");
		if($arg_pw == $pw) {
			$anzeige_id = get_get("anzeige_id");
			if($anzeige_id) {
				$link = get_get("link");
				$date = date("d.m.Y H:m:s");
				$reservierung_id = get_get("reservierung_id");
				$string = "$anzeige_id;$link;$date;$reservierung_id\n";

				if(file_exists($listings)) {
					$string .= file_get_contents($listings);
				}

				file_put_contents($listings, $string);
			}

			if(file_exists($listings)) {
				$handle = fopen($listings, "r");
				if ($handle) {
					print "<table><tr><th>Anzeige-ID</th><th>Link</th><th>Datum</th><th>Reservierungs-ID</th></tr>";
					while (($line = fgets($handle)) !== false) {
						// process the line read.
						$data_in_line = explode(";", $line);
						$anzeige_id = $data_in_line[0];
						$link = $data_in_line[1];
						$date = $data_in_line[2];
						$reservierung_id = $data_in_line[3];

						print "<tr><td>$anzeige_id</td><td><a href='https://ebay-kleinanzeigen.de/$link'>$link</a></td><td>$date</td><td>$reservierung_id</td></tr>";
					}

					fclose($handle);
					print "</table>";
				} else {
					die("ERROR opening $listings");
				}
			} else {
				die("Bisher keine Listings");
			}
		} else {
			die("Wrong password");
		}
	} else {
		die("No ".$pw_file." found");
	}
?>
