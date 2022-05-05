function randomInt (min, max) {
	return Math.floor(Math.random() * (max - min) + min);
}

function drawTestContainerOutline (ctx,x,y,width,height,strokeColor,fillColor ) {
	var radius = 2;

	ctx.lineWidth = 2;
	ctx.strokeStyle = strokeColor;
	ctx.beginPath();
	ctx.moveTo(x + radius, y);
	ctx.lineTo(x + width - radius, y);
	ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
	ctx.lineTo(x + width, y + height - radius);
	ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
	ctx.lineTo(x + radius, y + height);
	ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
	ctx.lineTo(x, y + radius);
	ctx.quadraticCurveTo(x, y, x + radius, y);
	ctx.closePath();
	if (fillColor ) {
		ctx.fillStyle = fillColor;
		ctx.fill();
	}

	var fontFamily = '"Lucida Console", Monaco, monospace';
	var fsize = 14;//size || 16;
	ctx.fillStyle = strokeColor;
	ctx.font=fsize+"px "+fontFamily; //'Palatino Linotype, Book Antiqua, Palatino, serif";//(fsize+"px "+ctx.font);

    ctx.stroke();



	ctx.lineWidth=1;
}

function drawContainer (ctx,x,y,width,height,color,v,density,units, disabled ) {
	var radius = 2;

	ctx.lineWidth = 2;
	ctx.strokeStyle = "rgb(74, 65, 57)";
	ctx.beginPath();
	ctx.moveTo(x + radius, y);
	ctx.lineTo(x + width - radius, y);
	ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
	ctx.lineTo(x + width, y + height - radius);
	ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
	ctx.lineTo(x + radius, y + height);
	ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
	ctx.lineTo(x, y + radius);
	ctx.quadraticCurveTo(x, y, x + radius, y);
	ctx.closePath();
	if (color ) {
		ctx.fillStyle = color;
		ctx.fill();
	}

	var fontFamily = '"Lucida Console", Monaco, monospace';
	var fsize = 14;//size || 16;
	ctx.fillStyle = "rgb(74, 65, 57)";
	ctx.font=fsize+"px "+fontFamily; //'Palatino Linotype, Book Antiqua, Palatino, serif";//(fsize+"px "+ctx.font);

	if (v)
	{
		ctx.fillText(v, x + 5, y + height - 5);
	}

    ctx.stroke();

	if (density) {
		ctx.lineWidth=0.5;
		//ctx.strokeStyle = "white";
		for (var j=0; j< units; j++) {
			ctx.fillText(density, x+j*config.cellSize + 6, y + height - 6);
			ctx.strokeRect(x + j*config.cellSize +0.5, y + 0.5, config.cellSize,config.cellSize);
		}
	}

	ctx.lineWidth=1;
}

function drawItem (ctx,x,y,item ) {
	var radius = 2;

	ctx.lineWidth = 2;

	ctx.strokeStyle = ACTIVE_TEST_LINE_COLOR;
	var height = config.cellSize;
	var width = item.w * config.cellSize;

	ctx.beginPath();
	ctx.moveTo(x + radius, y);
	ctx.lineTo(x + width - radius, y);
	ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
	ctx.lineTo(x + width, y + height - radius);
	ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
	ctx.lineTo(x + radius, y + height);
	ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
	ctx.lineTo(x, y + radius);
	ctx.quadraticCurveTo(x, y, x + radius, y);
	ctx.closePath();
	ctx.fillStyle = containerColors[item.position];

	ctx.fill();

	var fontFamily = '"Lucida Console", Monaco, monospace';
	var fsize = 14;//size || 16;
	ctx.fillStyle = "black";
	ctx.font=fsize+"px "+fontFamily; //'Palatino Linotype, Book Antiqua, Palatino, serif";//(fsize+"px "+ctx.font);


	ctx.fillText(item.v, x + 5, y + height - 5);
	ctx.stroke();

	ctx.lineWidth=1;
}



function strokeRoundedRectangle (ctx,x,y,width,height,lineWidth, color,r) {
	var radius = r || 5;
	ctx.lineWidth = lineWidth || 1;
	ctx.strokeStyle = color || "black";
	ctx.beginPath();
	ctx.moveTo(x + radius, y);
	ctx.lineTo(x + width - radius, y);
	ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
	ctx.lineTo(x + width, y + height - radius);
	ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
	ctx.lineTo(x + radius, y + height);
	ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
	ctx.lineTo(x, y + radius);
	ctx.quadraticCurveTo(x, y, x + radius, y);
	ctx.closePath();

    ctx.stroke();

	ctx.lineWidth=1;
}

function fillRoundedRectangle (ctx,x,y,width,height,color,r) {
	var radius = r || 5;

	ctx.fillStyle = color || "black";
	ctx.beginPath();
	ctx.moveTo(x + radius, y);
	ctx.lineTo(x + width - radius, y);
	ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
	ctx.lineTo(x + width, y + height - radius);
	ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
	ctx.lineTo(x + radius, y + height);
	ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
	ctx.lineTo(x, y + radius);
	ctx.quadraticCurveTo(x, y, x + radius, y);
	ctx.closePath();

    ctx.fill();

}
function strokeFrame (ctx,x,y,w,h,color, lineWidth) {
	ctx.lineWidth = lineWidth || 1;
	ctx.strokeStyle = color || "black";
	ctx.strokeRect(x + .5, y + .5, w,h);
}

function strokeLine (ctx, fromX, fromY, toX, toY, color, lineWidth){
	ctx.strokeStyle = color || "black";
	ctx.lineWidth = lineWidth || 2;
	ctx.beginPath ();
	ctx.moveTo (fromX, fromY);
	ctx.lineTo (toX, toY);
	ctx.stroke();
}

function fillRect (ctx, x, y, w, h, color) {
	ctx.fillStyle = color || "white";
	ctx.fillRect (x,y,w,h);
}

function drawTextCentre (ctx, text, x, y, color, size, font) {
	var fontFamily= font || WEB_SAFE_SIMPLE_SANS;
	var fsize = size || 24;
	ctx.textAlign = 'center';
	ctx.font=fsize+"px "+fontFamily; //'Palatino Linotype, Book Antiqua, Palatino, serif";//(fsize+"px "+ctx.font);

	ctx.fillStyle = color || "black";

	ctx.fillText(text, x + 5, y - 5);
}

//simple draw text - default sans=serif
function drawText (ctx, text, x, y, color, size, font) {
	var fontFamily = font || WEB_SAFE_SANS_SERIF;
	var fsize = size || 18;
	ctx.font= fsize+"px "+fontFamily; //'Palatino Linotype, Book Antiqua, Palatino, serif";//(fsize+"px "+ctx.font);
	ctx.fillStyle = color || DEFAULT_FONT_COLOR;
	ctx.fillText(text, x + 5, y - 5);
}
