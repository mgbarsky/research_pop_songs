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


function init(){
	
	// canvas = document.getElementById("canvas.heatmap");

	// ctx = canvas.getContext('2d');

	// canvas.width = (numCols +3) * config.cellWidth +3*config.offsetX; //window.innerWidth;;
	// canvas.height = (numRows+2) * config.cellHeight +4*config.offsetY+200;//window.innerHeight;

	// canvas.style.width = Math.min (canvas.width, Math.floor(0.8*window.innerWidth))+"px";
	
	data = reorderData(data);
	
	renderTable2 (data);
}

//compares 2 elements of the scores array
//to sort elements in descending order of scores
function compare_byscore_desc(a,b){
	if (a["score"] > b["score"]) {
		return -1;
	} else if (b["sum_score"] > a["sum_score"]) {
		return 1;
	}

	return 0;
}

function getTopKIndices(row,k){	
	var sorted = row.slice(0).sort(compare_byscore_desc);
	return sorted.slice(0, k);
}

function reorderData(data){
	var new_data = {};
	for (var i=0; i< data.length; i++){
		scores = new Array(data[i].length - 1);
		for(var j=1; j<data[i].length;j++){
			if (data[i][j] > maxDataValue)
				maxDataValue = data[i][j];
			scores[j-1] = {"score":data[i][j],"word":"sample word","index":j-1,"top":0};			
		}
		var top_elements = getTopKIndices(scores,5);
		for (var k=0; k<top_elements.length; k++){
			var elem = top_elements[k];
			var indx = elem["index"];
			scores[indx]["top"] = 1;
		}
		new_data["Country "+i]=scores;		
	}
	console.log("Max coount="+maxDataValue);
	return new_data;
}

function compare_bysum(a, b){
//compares 2 elements of a sum array by total score - to sort in descending order
  if (a["sum_score"] > b["sum_score"]) {
    return -1;
  } else if (b["sum_score"] > a["sum_score"]) {
    return 1;
  }

  return 0;
}


function say(word){
	console.log(word);
}

function renderTable2(data, bins){
	var el = document.getElementById("heattable");
	var table = document.createElement("table");
	table.className = "heattable";
	table.setAttribute("border","1");
	for (var i=0; i<countries.length; i++){
		var tr = document.createElement("tr");
		var td = document.createElement("td");
		var label = document.createElement("label");
		label.textContent = "Country "+i; //countries[i];
		label.setAttribute("class","countrylabel");
		td.appendChild(label);
		tr.appendChild(td);
		var scores = data["Country "+i];
		for (var j=0; j<scores.length; j++){
			var td = document.createElement("td");
			
			var cell = document.createElement("span");
			cell.className  = "countcell";
			
			cell.style.backgroundColor = getColorByValue(scores[j]);
			//TODO - display word when hovering
			td.appendChild(cell);
			tr.appendChild(td);
		}
		table.appendChild(tr);
	}
	el.appendChild(table);
}


function getColorByValue(score_obj){
	colors = ["#FFFFF0","#FFFFE0","#FFFACD","#FFF5EE","#FFEBCD","purple"];
	color = "white";
	if (score_obj["top"] == 1)
		 return "blue";
	var val = score_obj["score"];
	var rv = val / maxDataValue; //relative value
	var h = 60 + Math.floor(100 * rv),
	s = (1-rv) * (60) + 30;
	
	color = 'hsla('+ h +','+ s +'%,'+ 50 +'%,'+rv+')';
	return color;
	
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
