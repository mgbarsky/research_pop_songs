var top_words = [["Japan", "hello", "love", "burn", "right", "dance", "beat", "body", "night", "know", "running"], ["China", "love", "like", "know", "day", "lay", "simple", "worth", "melody", "girl", "mind"], ["India", "need", "tell", "girl", "love", "know", "good", "world", "give", "like", "sun"], ["Russia", "way", "day", "know", "love", "weekend", "hold", "club", "like", "come", "anymore"], ["Ukraine", "day", "know", "love", "like", "mind", "cause", "need", "feel", "look", "come"], ["Bulgaria", "like", "taste", "love", "know", "said", "need", "ring", "girl", "cause", "way"], ["Greece", "like", "love", "watch", "know", "tempo", "need", "said", "dance", "baby", "feel"], ["Argentina", "love", "like", "give", "hard", "know", "tell", "baby", "crazy", "calypso", "girl"], ["Chile", "like", "give", "hard", "love", "know", "tell", "baby", "look", "said", "calypso"], ["Brazil", "love", "come", "know", "crazy", "gave", "looking", "play", "heart", "affectionate", "baby"], ["Portugal", "like", "know", "taste", "love", "said", "need", "hand", "dim", "girl", "cause"], ["Spain", "like", "hard", "bad", "give", "know", "look", "time", "tell", "love", "calypso"], ["Italy", "like", "know", "love", "need", "come", "baby", "dance", "girl", "black", "sea"], ["France", "love", "like", "ciao", "air", "life", "need", "baby", "alright", "hand", "feel"], ["Belgium", "like", "know", "love", "need", "hard", "said", "cause", "look", "girl", "feel"], ["Switzerland", "like", "know", "love", "need", "born", "calypso", "said", "tell", "baby", "girl"], ["Finland", "like", "love", "know", "girl", "need", "cause", "touch", "gave", "way", "life"], ["Norway", "like", "love", "taste", "know", "need", "baby", "cause", "born", "fuck", "girl"], ["Denmark", "like", "know", "taste", "love", "said", "need", "baby", "happy", "come", "cause"], ["Sweden", "taste", "like", "know", "need", "love", "born", "girl", "baby", "rise", "touch"], ["Netherlands", "know", "love", "like", "air", "come", "bitch", "hard", "need", "tell", "give"], ["Austria", "like", "know", "baby", "life", "come", "bra", "love", "need", "cause", "girl"], ["German", "like", "baby", "look", "love", "know", "need", "child", "ball", "come", "bra"], ["Ireland", "like", "know", "love", "taste", "said", "need", "baby", "cause", "girl", "heart"], ["UK Singles", "like", "know", "love", "need", "baby", "girl", "said", "feel", "cause", "rise"], ["USA Singles", "like", "taste", "baby", "love", "said", "know", "girl", "need", "high", "cause"], ["Canada", "like", "know", "taste", "said", "love", "need", "cause", "girl", "friend", "bitch"], ["Australia", "know", "love", "like", "cause", "need", "baby", "hand", "said", "tell", "away"], ["New Zealand", "like", "know", "love", "taste", "said", "vibe", "need", "baby", "heart", "girl"]];
var countries = [
"Brazil",
"Russia",
"Italy",
"Argentina",
"Chile",
"Spain",
"Greece",
"Netherlands",
"France",
"Ukraine",
"Austria",
"German",
"Switzerland",
"Belgium",
"Finland",
"UK Singles",
"Sweden",
"Norway",
"Denmark",
"Ireland",
"Australia",
"New Zealand",
"Bulgaria",
"Portugal",
"Canada",
"USA Singles",
"Japan",
"China",
"India"
];

var config = {
	cellSize: 40,
	cellWidth: 60,
	cellHeight: 150,
	legendOffsetX: 0,
	legendOffsetY: 10,
	offsetX: 10,
	offsetY: 0
};

//font constants and defaults
var DEFAULT_FONT_COLOR ="rgba(0,0,0,.75)";
var WEB_SAFE_SERIF = '"Palatino Linotype", "Book Antiqua", Palatino, serif';
var WEB_SAFE_SANS_SERIF = '"Lucida Sans Unicode", "Lucida Grande", sans-serif';
var WEB_SAFE_SIMPLE_SANS = 'Verdana, Geneva, sans-serif';
var WEB_SAFE_MONOSPACE ='"Lucida Console", Monaco, monospace';
var WEB_SAFE_IMPACT = 'Impact, Charcoal, sans-serif';

var maxDataValue = 0;

var index_to_word = [];
function init(){
	
	// canvas = document.getElementById("canvas.heatmap");

	// ctx = canvas.getContext('2d');

	// canvas.width = (numCols +3) * config.cellWidth +3*config.offsetX; //window.innerWidth;;
	// canvas.height = (numRows+2) * config.cellHeight +4*config.offsetY+200;//window.innerHeight;

	// canvas.style.width = Math.min (canvas.width, Math.floor(0.8*window.innerWidth))+"px";
	
	var data = reorderData(top_words);
	
	renderTable2 (data);
}


function reorderData(word_list){
	//collect all distinct words into dictionary	
	var word_to_index = {};
	var count =0;
	for (var i=0; i < word_list.length; i++){
		for (var j=1;j<word_list[i].length;j++){
			w = word_list[i][j];
			if (!word_to_index.hasOwnProperty(w))	
				word_to_index[w] = count++;
		}			
	}
	
	//console.log(count);
	index_to_word = new Array(count);
	
	for (var key in word_to_index) {
		// check if the property/key is defined in the object itself, not in parent
		if (word_to_index.hasOwnProperty(key)) {           
			pos = word_to_index[key];
			index_to_word[pos] = key;
		}
	}
	
	new_data = {};
	for (var i=0; i< word_list.length; i++){
		country = word_list[i][0];
		words = new Array(count);
		for (var k=0; k< count; k++){
			words[k] = 0;
		}
		for (var j=1;j<word_list[i].length;j++){
			w_idx = word_to_index[word_list[i][j]];
			words[w_idx]=1;
		}
		new_data[country] = words;
	}
	
	// console.log(new_data);
	
	return new_data;
}


function renderTable2(data, bins){
	var el = document.getElementById("heattable");
	var table = document.createElement("table");
	table.className = "heattable";
	//table.setAttribute("border","1");
	for (var i=0; i<countries.length; i++){
		var tr = document.createElement("tr");
		var td = document.createElement("td");
		var label = document.createElement("label");
		label.textContent = countries[i];
		label.setAttribute("class","countrylabel");
		td.appendChild(label);
		tr.appendChild(td);
		var scores = data[countries[i]];
		for (var j=0; j<scores.length; j++){
			var td = document.createElement("td");
			
			var cell = document.createElement("span");
			cell.className  = "countcell";
			
			cell.style.backgroundColor = getColorByValue(scores[j]);
			if (scores[j] == 1){
				cell.setAttribute("title",index_to_word[j]);
			}
			//TODO - display word when hovering
			td.appendChild(cell);
			tr.appendChild(td);
		}
		table.appendChild(tr);
	}
	el.appendChild(table);
}


function getColorByValue(score){
	colors = ["#FFFFF0","#FFFFE0","#FFFACD","#FFF5EE","#FFEBCD","purple"];
	color = "white";
	if (score == 1)
		 return "#A61646";
	else
		return "#FFC7B3";	
	
}

function renderCell (ctx, x,y,  value, maxValue, showValue) {
	// var rv = value / maxValue; //relative value
	// var h = 70 + Math.floor(100 * rv),
	// 	s = (1-rv) * (50) + 30;
	//
	// var color = 'hsla('+ h +','+ s +'%,'+ 50 +'%,'+rv+')';
	// if (value < 0.03){
	// 	var color = 'rgb(230, 242, 255)';
	// } else if (value < 0.06){
	// 	var color = 'rgb(153, 187, 255)';
	// } else if (value < 0.09){
	// 	var color = 'rgb(102, 140, 255)';
	// } else if (value < 0.12){
	// 	var color = 'rgb(51, 51, 255)';
	// } else{
	// 	var color = 'rgb(0, 0, 153)';
	// }

	if (value < 0.03){
		var color = 'yellow)';
	} else if (value < 0.06){
		var color = 'orange';
	} else if (value < 0.09){
		var color = 'green';
	} else if (value < 0.12){
		var color = 'purple';
	} else{
		var color = 'blue';
	}

	//ctx.globalAlpha = 0.8;

	fillRect (ctx, x, y, config.cellWidth, config.cellHeight, color);


	//strokeFrame (ctx,x,y,config.cellSize, config.cellSize,"rgba(215,215,215,0.5)");

	if (showValue)
		drawCellValue (ctx, value, x, y+config.cellHeight);
	ctx.globalAlpha = 1;
}


function renderTable (data, maxValue){
	for (var i=0; i< data.length; i++) {
		y = 3*config.offsetY + 2*config.cellHeight+ i * config.cellHeight;
		var x = config.offsetX;
		drawText (ctx, 'country1', x, y+120, 'red', 150, WEB_SAFE_SERIF);
		for (var j=0; j<data[i].length; j++){
			var x = config.offsetX + j * config.cellWidth+700;

			renderCell(ctx, x,y, data[i][j], maxValue);
		}
	}
}

//simple small corner-cell monospace font
function drawCellValue (ctx, value, x, y) {
	drawText (ctx, value, x, y, DEFAULT_FONT_COLOR, 10, WEB_SAFE_MONOSPACE);
}

function drawTableHeader (ctx, text, x, y) {
	drawText (ctx, text, x, y, "black", 18, WEB_SAFE_SERIF);
}

function drawHeader (ctx, text, x, y) {
	drawText (ctx, text, x, y, "black", 12, WEB_SAFE_SERIF);
}

function drawTitle (ctx, text, x, y) {
	drawText (ctx, text, x, y, "black", 18, WEB_SAFE_SERIF);
}

function drawSubtitle (ctx, text, x, y) {
	ctx.globalAlpha=1;

	drawText (ctx, text, x, y, "black", 16, WEB_SAFE_SERIF);
}

/**
 * Returns a random integer between min (inclusive) and max (inclusive)
 * Using Math.round() will give you a non-uniform distribution!
 */
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function generateSampleData(){
	var data = new Array(20);

	for (var i=0; i< 20; i++){
		data[i] = new Array(200);
	}

	for (var i=0; i< 20; i++){
		for (var j=0; j< 200; j++)
			data[i][j] = getRandomInt(10, maxDataValue) ;
	}
	return data;
}
