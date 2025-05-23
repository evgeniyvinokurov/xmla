let ToolsService = {
	doByClassName: function(className, cb) {
		let elems = document.getElementsByClassName(className);

    	for (let i = 0; i < elems.length; i += 1) {
    		let elemItem = elems[i];
    		cb(elemItem);
    	}

    	return  elems;
	},
	getRandomNumber: function() {
		return Math.floor((Math.random() * 9999999) + 1111111);
	},
	getRandomFloat: function(min, max, decimals) {
  		let str = (Math.random() * (max - min) + min).toFixed(decimals);
  		return parseFloat(str);
	},
	getRandomColor: function() {
		var letters = '0123456789';
	    var number = 'rgba(';
	    for (var i = 0; i < 3; i += 1 ) {
	        number += Math.floor(Math.random() * 255) + ",";
	    }
	    number += "0.4)"
	    return number;
	},
	getRandomArrayValue: function(array){
		var choose = [];

	  for (var key in array) {
	    	choose.push(key);
		}

		var arrayLength = choose.length;
		return array[choose[Math.floor(Math.random() * arrayLength)]];
	},
	getRandom: function(min, max) {
		var x = Math.ceil(Math.random() * (max - min) + min);
		if (max == x) {
			x -= 1;
		}
		return x;
	},
	getFromWarmColors: function(){
		let colors = ["#8B8989","#CDC9C9","#EEE9E9","#8B6969","#856363","#6F4242","#BC8F8F","#CD9B9B","#8B3A3A","#C67171","#802A2A","#CD5C5C","#CD5555","#A52A2A","#8B2323","#8E2323","#A62A2A","#CD3333","#CC3232","#EEB4B4","#BE2625","#8B1A1A","#B22222","#CD2626","#DB2929","#8C1717","#F08080","#EE6363","#EE3B3B","#EE2C2C","#330000","#660000","#800000","#8B0000","#CD0000","#EE0000","#FF0000","#FF3030","#FF3333","#FF4040","#FF6666","#FF6A6A","#FFC1C1","#FFCCCC","#FFFAFA","#A02422","#C65D57","#D44942","#F2473F","#E3170D","#9D1309","#CDB7B5","#AF4035","#ECC3BF","#FC1501","#CC1100","#EED5D2","#FA8072","#FFE4E1","#8B7D7B","#D66F62","#C75D4D","#FF2400","#8A3324","#CD4F39","#EE5C42","#FF5333","#FF6347","#B0A6A4","#8B3E2F","#8B3626","#CD5B45","#EE6A50","#FF7256","#B3432B","#D43D1A","#F5785A","#FF3300","#FF3D0D","#8B4C39","#CD7054","#C73F17","#EE8262","#FF8C69","#A78D84","#E9967A","#FF5721","#5E2612","#E04006","#8B2500","#CD3700","#EE4000","#FF4500","#FF7F50","#8B5742","#CD8162","#EE9572","#B13E0F","#691F01","#FFA07A","#5C4033","#D19275","#A0522D","#CD6839","#8A360F","#EE7942","#FF7D40","#FF8247","#8B4726","#DB9370","#87421F","#993300","#F87531","#292421","#97694F","#5E2605","#FBA16C","#FF6103","#964514","#E47833","#FF7722","#6B4226","#5C3317","#733D1A","#FF6600","#FF7216","#FF9955","#A68064","#855E42","#E9C2A6","#CD661D","#D2691E","#8B4513","#EE7621","#FF7F24","#FFF5EE","#CDC5BF","#EEE5DE","#BC7642","#603311","#E3701A","#C76114","#FA9A50","#8B8682","#EE8833","#FEE8D6","#B6AFA9","#8B7765","#CDAF95","#EECBAD","#F4A460","#FFDAB9","#8B5A2B","#B87333","#EE9A49","#AA5303","#FFA54F","#E7C6A5","#CD853F","#CD7F32","#CC7F32","#FAF0E6","#CC7722","#8B4500","#CD6600","#EE7600","#FF8000","#FF7F00","#FFCC99","#C9AF94","#362819","#B67C3D","#C77826","#E3A869","#E38217","#7B3F00","#CDB79E","#9F703A","#EBCEAC","#EBC79E","#EDC393","#E18E2E","#C76E06","#DD7500","#FF8600","#CDC0B0","#8B7355","#EED5B7","#DFAE74","#ED9121","#FF8C00","#FFE4C4","#FFEFDB","#8B7D6B","#A39480","#CDAA7D","#D2B48C","#EEDFCC","#C48E48","#DEB887","#9C661F","#EEC591","#FAEBD7","#D98719","#FCE6C9","#FF9912","#FFD39B","#8B8378","#B28647","#734A12","#8B795E","#CDB38B","#EECFA1","#DC8909","#FCD59C","#FEF0DB","#AA6600","#FFA824","#FFC469","#FFDEAD","#FFEBCD","#A67D3D","#EED6AF","#FFEFD5","#FFA812","#FFE4B5","#8B7E66","#8C7853","#CDBA96","#EED8AE","#F5DEB3","#FDF5E6","#8B5A00","#CD8500","#EE9A00","#FFA500","#FFE7BA","#D5B77A","#8E6B23","#AC7F24","#FFAA00","#FFB00F","#FFFAF0","#E8C782","#F0A804","#FCB514","#FEE5AC","#FFB90F","#9D8851","#DAA520","#8B6914","#CD9B1D","#EEB422","#8B6508","#B8860B","#CD950C","#EEAD0E","#FFC125","#E6B426","#EDCB62","#E5BC3B","#CDAB2D","#FFCC11","#E0DFDB","#FFF8DC","#C6C3B5","#CDC8B1","#EEE8CD","#CFB53B","#FCD116","#FEF1B5","#8B814C","#CDBE70","#EEDC82","#FCDC3B","#FFEC8B","#8B8878","#C5C1AA","#E3CF57","#EEDD82","#8B7500","#CDAD00","#EEC900","#FFD700","#B5A642","#FBDB0C","#E2DDB5","#F3E88E","#FFE303","#CDC9A5","#EEE9BF","#D6C537","#F0E68C","#FBEC5D","#FFE600","#FFFACD","#615E3F","#8B864E","#CDC673","#EEE8AA","#EEE685","#FFF68F","#8B8970","#BDB76B","#E0D873","#BAAF07","#FFFCCF","#CBCAB6","#EEEB8D","#7B7922","#CECC15","#3A3A38","#8B8B83","#8B8B7A","#808069","#CDCDC1","#CDCDB4","#D8D8BF","#4F4F2F","#9F9F5F","#EEEEE0","#777733","#8E8E38","#EEEED1","#F5F5DC","#EAEAAE","#DBDB70","#D9D919","#FAFAD2","#808000","#8B8B00","#CDCD00","#CCCC00","#EEEE00","#FFFF00","#FFFF7E","#FFFFAA","#FFFFCC","#FFFFE0","#FFFFF0","#F4F776","#CDD704","#98A148","#CFD784","#D1E231","#AEBB51","#D0D2C4","#A2BC13","#B3C95A","#859C27","#CDE472","#FCFFF0","#C8F526","#414F12","#668014","#AADD00","#BCE937","#54632C","#8BA446","#A2C93A","#D4ED91","#BEE554","#9CCB19","#A2C257","#E8F1D4","#698B22","#79973F","#6B8E23","#99CC32","#9ACD32","#B3EE3A","#C0FF3E","#DFFFA5","#556B2F","#6E8B3D","#A2CD5A","#BCEE68","#CAFF70","#ADFF2F"];
		return this.getRandomArrayValue(colors);
	}
};

export { ToolsService };
