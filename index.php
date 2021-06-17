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

	$udst_route = "logo-usdt.png";
	$crypto_route = "logo-";
	if (isset($pair["symbol"])) {
		$newphrase = str_replace("USDT", "", $pair["symbol"]);
		$crypto_route = $crypto_route . strtolower($newphrase) . ".png";
	}

?>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">

		<link rel="stylesheet" type="text/css" href="css/util.css">
		<link rel="stylesheet" type="text/css" href="css/main.css">

		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
		<link rel="stylesheet" href="css/custom-style.css">

		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>

		<body class = "bg-light">
		




<!--
<div id="actions">
<select id="options">
  <option value="" disabled selected>Select an option</option>
  <option value="TRADING">TRADING</option>
  <option value="ARBITRAJE">ARBITRAJE</option>
</select>

<select id="choices">
  <option value="" disabled selected>Please select an option</option>
</select>
</div>
<div id="cripto">CRIPTOMONEDA:<input type="text" size="10" id="campo" name="campo"/></div>

<button class="btn" onclick="play()"><i class="fa fa-play"></i></button>
<button class="btn" onclick="stop()"><i class="fa fa-stop"></i></button>
-->




		<div class="limiter">
		<div class="container-login100">
		<div class="wrap-login100" style="padding-bottom: 3%!important; ">
		



			<div class ="col-sm-12">
				<img class="d-block mx-auto mb-4" src="https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg" alt="" width="72" height="72">
			</div>
			
			<div class ="col-sm-12 extra">
				<form class="myform">
			  
					<select id="options" class="custom-select">
					  <option value="" disabled selected>Select an option</option>
					  <option value="TRADING">TRADING</option>
					  <option value="ARBITRAJE">ARBITRAJE</option>
					</select><br><br>
					<select id="choices" class="custom-select">
					  <option value="" disabled selected>Please select an option</option>
					</select><br><br>
					<div id="cripto">
						<label for="criptomoneda">CRIPTOMONEDA:</label>
  						<input type="text" id="campo" name="campo"><br>
					</div>
					<div class="center">
						<button class="btn" onclick="play()"><i class="fa fa-play"></i></button>
						<button class="btn" onclick="stop()"><i class="fa fa-stop"></i></button>
					</div>
				</form>
			</div>




			<div class="container">
				<div class="py-5 text-center" style="padding-top: 0!important; ">
					<h2><?php echo $mode;?></h2>
					<p class="lead"><?php echo $election;?></p>
				</div>

				<div class="d-flex justify-content-center">
					<div class="col-sm-7 text-center description-text" style="background:white;">	
						<div class="row" style="border-radius: 10px;box-shadow: 0 0 25px 10px grey">
							<?php
							if (isset($pair["symbol"])) {
								if ($mode == "TRADING MODE") {
									if ($pair["state"] == 0) 
										echo '				
										<div id="containerLogo" class="col-md-4">
											<p><img src="img/logos-criptos/'.$udst_route.'" 
													width="140" height="120" frameBorder="0"></p>
										</div>

										<div id="containerIcon" class="col-md-4">
											<p><iframe src="https://giphy.com/embed/rDb9zTgdfiPwQ" 
													width="100" height="180" frameBorder="0"></iframe></p>
										</div>
										
										<div id="containerLogo" class="col-md-4">
											<p><img src="img/logos-criptos/'.$crypto_route.'" 
													width="100" height="120" frameBorder="0"></p>
										</div>
										';
									else
										echo '				
										<div id="containerLogo" class="col-md-12">
											<p><img src="img/logos-criptos/'.$udst_route.'" 
													width="140" height="120" frameBorder="0"></p>
										</div>
										';
								} else
									if ($election == "ARBITRAGE WITH TRANSFERENCE") {
										if ($pair["state"] == 0)  
										echo '
										<div id="containerLogo" class="col-md-4"><div><b>BINANCE</b></div>
											<p><img src="img/logos-criptos/'.$udst_route.'" 
												width="140" height="120" frameBorder="0"></p>
										</div>

										<div id="containerIcon" class="col-md-4">
											<p><iframe src="https://giphy.com/embed/rDb9zTgdfiPwQ" 
													width="100" height="180" frameBorder="0"></iframe></p>
										</div>
										
										<div id="containerLogo" class="col-md-4"><div><b>KUCOIN</b></div>
											<p><img src="img/logos-criptos/'.$crypto_route.'" 
													width="100" height="120" frameBorder="0"></p>
										</div>
										';
										else
											echo '
											<div id="containerLogo" class="col-md-12"><div><b>ACTUALMENTE NO ESTÁ REALIZANDO ARBITRAJE</b></div>
												<p><img src="img/logos-criptos/'.$udst_route.'" 
													width="140" height="120" frameBorder="0"></p>
											</div>
											';
									} else
										if (isset($pair['way']) && $pair['way'] == 0)
										echo '
										<div id="containerLogo" class="col-md-6"><div><b>BINANCE</b></div>
											<div><img class="img-fluid" src="img/logos-criptos/'.$crypto_route.'"></div>
										</div>

										<div id="containerLogo" class="col-md-6"><div><b>KUCOIN</b></div>
											<img class="img-fluid" src="img/logos-criptos/'.$udst_route.'">
										</div>
										';
										else if (isset($pair['way']) && $pair['way'] == 1)
										echo '
										<div id="containerLogo" class="col-md-6"><div><b>BINANCE</b></div>
											<div><img class="img-fluid" src="img/logos-criptos/'.$udst_route.'"></div>
										</div>

										<div id="containerLogo" class="col-md-6"><div><b>KUCOIN</b></div>
											<img class="img-fluid" src="img/logos-criptos/'.$crypto_route.'">
										</div>
										';
							} 
							?>
						</div>
					</div>
				</div><br><br>
			</div>
			<?php
					if (!isset($pair["symbol"])) { 
						echo '
						<div class="d-flex justify-content-center" style="padding: 0 1rem; margin: 1rem;">
									ACTUALMENTE NO ESTÁ TRABAJANDO CON NINGÚN PAR
						</div>
						';
					}
			?>

			</div>
			</div>
			</div>

        </body>
	</head>    
							
    <!--<footer class="my-5 pt-5 text-muted text-center text-small">
        <p class="mb-1">© Trading Bot</p>
        <ul class="list-inline">
          	<li class="list-inline-item"><a href="#">Privacy</a></li>
          	<li class="list-inline-item"><a href="#">Terms</a></li>
          	<li class="list-inline-item"><a href="#">Support</a></li>
        </ul>
    </footer>-->

</html>


<script>
// Map your choices to your option value
var lookup = {
   'TRADING': ['Estrategia Customizada', 'Estrategia basada en EMA', 'Estrategia basada en patron envolvente'],
   'ARBITRAJE': ['Arbitraje con transferencia', 'Arbitraje compra/venta'],
};

// When an option is changed, search the above for matching choices
$('#options').on('change', function() {
   // Set selected option as variable
   var selectValue = $(this).val();

   // Empty the target field
   $('#choices').empty();
   
   // For each choice in the selected option
   for (i = 0; i < lookup[selectValue].length; i++) {
      // Output choice in the target field
      $('#choices').append("<option value='" + lookup[selectValue][i] + "'>" + lookup[selectValue][i] + "</option>");
   }
});


var control;

function check(value) {
	control = value;
}

function play() {
	
	$.ajax({
		url: "req/check-start.php",
		async: false,
		success: function(output) {
			check(output);
			//alert(output);
		}
	});

	if (control != '1' && control != '2') {
		var m = document.getElementById("options");
		var o = document.getElementById("choices");

		var modo = m.value;
		var opcion = o.value;

		if (modo == "TRADING") {
			modo = 1;
			if (opcion == "Estrategia Customizada")
				opcion = 1;
			else if (opcion == "Estrategia basada en EMA")
				opcion = 2;
			else if (opcion == "Estrategia basada en patron envolvente")
				opcion = 3;
			else 
				opcion = 0;
		} else if (modo == "ARBITRAJE") { 
			modo = 2;
			if (opcion == "Arbitraje con transferencia")
				opcion = 1;
			else if (opcion == "Arbitraje compra/venta")
				opcion = 2;
			else 
				opcion = 0;
		} else {
			modo = 0;
			opcion = 0;
		}
		
		var cripto = document.getElementById("campo");

		$.ajax({
			type: 'POST',
			url: "req/get-start.php",
			data: {
				modo: modo,
				opcion: opcion
			},
			success: function(output) {
				//alert(output);
			}
		});

		//console.log("play");
		$.ajax({
			url: "main.py",
			method: 'post',
			success: function(data)
			{
				alert(data);
			}
		});
	}
	else {
		alert("Debe parar primero el programa");
	}
	
}

function stop() {
	console.log("stop");
	var invocation = new XMLHttpRequest();
	var url = 'http://localhost:8000/stop';

	if(invocation) {
		invocation.open('GET', url, true);
		//invocation.onreadystatechange = handler;
		invocation.send();
	}
}


setTimeout(function(){
   window.location.reload(1);
}, 5000);
</script>

