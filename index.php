<?php 
include "functions.php"
?>

<?php
	$mode_info = get_mode();
	$mode = "";
	$election = "";
	if (isset($mode_info["type"]) && $mode_info["type"] == 1)
	{
		$mode = "TRADING MODE";
		if ($mode_info["election"] == 1)
		{
			$election = "CUSTOM STRATEGY";
			
		} else if ($mode_info["election"] == '2')
		{
			$election = "EMA STRATEGY";
		} else if ($mode_info["election"] == '3')
		{
			$election = "ENGULFING PATTERN STRATEGY";
		}
	} else if (isset($mode_info["type"]) && $mode_info["type"] == 2)
	{
		$mode = "ARBITRAGE MODE";
		if ($mode_info["election"] == '1')
		{
			$election = "ARBITRAGE WITH TRANSFERENCE";
			
		} else if ($mode_info["election"] == '2')
		{
			$election = "BUY/SELL ARBITRAGE (STAKING)";
		}
	}
	$pair = get_actual_pair($mode);
	$crypto_route = "logo-";
	if (isset($pair["symbol"])) {
		$newphrase = str_replace("USDT", "", $pair["symbol"]);
		$crypto_route = $crypto_route . strtolower($newphrase) . ".png";
	}
	print_r($crypto_route);

?>
<html>
	<head>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
		<link rel="stylesheet" href="css/custom-style.css">

		<body class = "bg-light">
			<div class="container" >
				<div class="py-5 text-center">
					<img class="d-block mx-auto mb-4" src="https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg" alt="" width="72" height="72">
					<h2><?php echo $mode;?></h2>
					<p class="lead"><?php echo $election;?></p>
				</div>

				<div class="d-flex justify-content-center">
					<div class="col-sm-7 text-center description-text" style="background:white;">	
						<div class="row" style="border-radius: 10px;box-shadow: 0 0 25px 10px grey">
							<?php
							if ($mode == "TRADING MODE") 
								echo '				
								<div id="containerLogo" class="col-md-4">
									<p><img src="img/logos-criptos/logo-usdt.png" 
											width="140" height="120" frameBorder="0"></p>
								</div>

								<div id="containerIcon" class="col-md-4">
									<p><iframe src="https://giphy.com/embed/rDb9zTgdfiPwQ" 
											width="100" height="180" frameBorder="0"></iframe></p>
								</div>
								
								<div id="containerLogo" class="col-md-4">
									<p><img src="img/logos-criptos/logo-eth.png" 
											width="100" height="120" frameBorder="0"></p>
								</div>
								';
							else
							
								if ($election == "ARBITRAGE WITH TRANSFERENCE") 
									echo '
									<div id="containerLogo" class="col-md-4"><div><b>BINANCE</b></div>
										<p><img src="img/logos-criptos/logo-usdt.png" 
												width="140" height="120" frameBorder="0"></p>
									</div>

									<div id="containerIcon" class="col-md-4">
										<p><img src="img/logos-criptos/flecha-imagen-arb.gif" 
												width="70" height="85" frameBorder="0"></p>
									</div>
									
									<div id="containerLogo" class="col-md-4"><div><b>KUCOIN</b></div>
										<p><img src="img/logos-criptos/logo-eth.png" 
												width="100" height="120" frameBorder="0"></p>
									</div>
									';
								else 
									echo '
									<div id="containerLogo" class="col-md-6"><div><b>BINANCE</b></div>
										<div><img class="img-fluid" src="img/logos-criptos/logo-usdt.png"></div>
									</div>

									<div id="containerLogo" class="col-md-6"><div><b>KUCOIN</b></div>
										<img class="img-fluid" src="img/logos-criptos/logo-eth.png">
									</div>
									';
							?>
						</div>
					</div>
				</div>
			</div>
        </body>
	</head>    
							
    <footer class="my-5 pt-5 text-muted text-center text-small">
        <p class="mb-1">© Trading Bot</p>
        <ul class="list-inline">
          	<li class="list-inline-item"><a href="#">Privacy</a></li>
          	<li class="list-inline-item"><a href="#">Terms</a></li>
          	<li class="list-inline-item"><a href="#">Support</a></li>
        </ul>
    </footer>

</html>

<script>
/*setTimeout(function(){
   window.location.reload(1);
}, 5000);*/
</script>
