/* ------------------------------------------------------------------------
- A Custom JS File uses JSXGraph - https://jsxgraph.uni-bayreuth.de/wp/about/index.html
--------------------------------------------------------------------------*/
var turtle = null;
var alpha = 0;

function load_map()
{
   var width = screen.width * 0.45;
    var brd = JXG.JSXGraph.initBoard('box',{ boundingbox: [-width, 300, width, -300], keepaspectratio:true });
    turtle = brd.create('turtle',[0, 0], {strokeOpacity:0.5});
    turtle.setPenSize(3);
    turtle.right(90);
}

function mapForward(results)
{
   turtle.lookTo(results.heading);
   turtle.forward(results.elapsedtime*50);
}
function mapBackward(results)
{
   turtle.lookTo(results.heading);
   turtle.forward(results.elapsedtime*-50);
}

load_map();
