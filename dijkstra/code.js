
// const COLS = 5;
// const ROWS = 5;

/*

      Ivan's original algorithm

*/

// run_the_algorithm(COLS, ROWS)


function run_the_algorithm(COLS, ROWS, dead_node=-1){

    
var data = [];

function node() 
    {
        this.west = 1;
        this.north = 1;
        this.east = 1;
        this.south = 1;
        this.value = 0;
        this.path = 0;
        this.closest_origin = 0;
        this.dead = false;
    }

var nodes_original = new Array();
for (var k = 0; k < COLS*ROWS; k++)
{
    nodes_original.push(new node());
    // if(dead_node == k) nodes_original[k].dead = true;
}


// calculate_nodes_original()
display_grid()


// use Dijkstra algorithm to calculate all weights



function display_grid(){

    var i, j;
    for (i = 0; i < COLS; i++) {
      for (j = 0; j < ROWS; j++) {
        data.push( {
          "data": {
            "id": "n-"+i+"-"+j,
            "weight": j*COLS+i,
            // "label": "non"
          },
          "position": {
            "x": 50+110*i,
            "y": 50+110*j
          },
          "group": "nodes",
          "removed": false,
          "selected": false,
          "selectable": true,
          "locked": false,
          "grabbable": true,
          // if the node is dead, then assign "dead" class which makes the colo red
          "classes": (dead_node==j*COLS+i)?"dead":""
           // "classes": nodes_original[j*COLS+i].dead?"dead":""
        });
      }
    }

    // two for loops for creating edges

    for (i = 0; i < COLS; i++) {
      for (j = 0; j < ROWS; j++) {
          if(j != ROWS-1) { // if the element is not at the last row
          data.push({
            "data": {
              "id": "e-"+i+"-"+j+"--"+i+"-"+(j+1),
              "weight": 1,
              "source": "n-"+i+"-"+j,
              "target": "n-"+i+"-"+(j+1),
              "label": nodes_original[j*COLS+i].south
            },
            "position": {},
            "group": "edges",
            "removed": false,
            "selected": false,
            "selectable": true,
            "locked": true,
            "grabbable": true,
            "classes": "outline"
          });
        }
        else // if the element is  at the last row -- wrap around to the 0th row
        {
          data.push({
            "data": {
              "id": "e-"+i+"-"+j+"--"+i+"-"+0,
              "weight": 1,
              "source": "n-"+i+"-"+j,
              "target": "n-"+i+"-"+0,
              "label": nodes_original[j*COLS+i].south
            },
            "position": {},
            "group": "edges",
            "removed": false,
            "selected": false,
            "selectable": true,
            "locked": true,
            "grabbable": true,
            "classes": "outline unbundled-bezier"
          });
        }


          if(i != COLS-1) { // if the element is not at the last row
          data.push({ 
            "data": {
              "id": "e-"+i+"-"+j+"--"+(i+1)+"-"+j,
              "weight": 1,
              "source": "n-"+i+"-"+j,
              "target": "n-"+(i+1)+"-"+j,
              "label": nodes_original[j*COLS+i].east
            },
            "position": {},
            "group": "edges",
            "removed": false,
            "selected": false,
            "selectable": true,
            "locked": true,
            "grabbable": true,
            "classes": "outline"
          });
        }

        else { // if the element is at the last row -- wrap around
          data.push({ 
            "data": {
              "id": "e-"+i+"-"+j+"--"+0+"-"+j,
              "weight": 1,
              "source": "n-"+i+"-"+j,
              "target": "n-"+0+"-"+j,
              "label": nodes_original[j*COLS+i].east
            },
            "position": {},
            "group": "edges",
            "removed": false,
            "selected": false,
            "selectable": true,
            "locked": true,
            "grabbable": true,
            "classes": "outline unbundled-bezier"
          });
        }
      }
    }

    console.log(data);


    var cy = window.cy = cytoscape({
      container: document.getElementById('cy'),

      boxSelectionEnabled: false,
      autounselectify: true,

      layout: {
        name: 'preset'
      },

      style: [
            {
            selector: 'node',
            style: {
              'height': 20,
              'width': 20,
              'background-color': '#18e018'
            }
            },

            {
            selector: 'edge',
            style: {
              'curve-style': 'haystack',
              'haystack-radius': 0,
              'width': 5,
              'opacity': 0.5,
              'line-color': '#a2efa2'
            }
            },
            {
            selector: "node[label]",
            style: {
            "label": "data(label)"
            }
            },

            {
            selector: "edge[label]",
            style: {
            'label': "data(label)",
            'width': 3
            }
            },

            {
            selector: ".outline",
            style: {
            'color': "#fff",
            'text-outline-color': "#888",
            'text-outline-width': 3
            }
            },

            {
            selector: ".dead",
            style: {
            'color': "#fff",
            'text-outline-color': "#888",
            'text-outline-width': 3,
            'background-color': '#e01717'
            }
            },

            {
            selector: "edge.unbundled-bezier",
            style: {
              "curve-style": "unbundled-bezier",
              "control-point-distances": 120,
              "control-point-weights": 0.1
            }
            }



      ],

      elements: data
    });

    // highlight the node which we clicked on
    cy.on('tap', 'node', function(evt){
      var node = evt.target;
      // console.log( 'tapped ' + JSON.stringify(node.json()) );
      // console.log( 'tapped ' + JSON.stringify(node.json()) );
      var node_json = JSON.stringify(node.json());
      var index_of_weight = node_json.indexOf("weight")
      var dead_node_id = parseInt(node_json.substring(index_of_weight+8, index_of_weight+11));
      run_the_algorithm(parseInt(COLS), parseInt(ROWS), dead_node_id);
    });



    // calculate the weights using minimal path algorithm
    // var dijkstra = cy.elements().dijkstra('#n-0-0', function(edge){
    //         return edge.data('weight');});
    var i, j;
    for (i = 0; i < COLS; i++) {
      for (j = 0; j < ROWS; j++) {
        if(i==0 & j==0) continue; // skip the master

        var aStar = cy.elements().aStar({ root: "#n-0-0", goal: "#n-"+i+"-"+j, weight: function(edge){
  return edge.data('weight');
} });
        if (aStar.distance > (i+j)){ 
          console.log("ERROR: THE MINIMAL PATH IS LONGER THAN MINIMIUM HOP COUNT");
          console.log("the hop count is " + (i+j) + " as x = " + i + " and y = " + j);
          console.log("but the distance " + aStar.distance);
          console.log(aStar.path);
        }
        if (!aStar.found) console.log("ERROR: MINUMUM PATH NOT FOUND");

            // console.log(aStar.path);
            var k;
            for ( k=0; k<aStar.path.length; k++ ) {  
                if(aStar.path[k].isEdge()){ 
                    //console.log(aStar.path[k].id());
                    //chnage the weigth
                    // console.log(cy.$("#"+aStar.path[k].id()).data());
                    // console.log(cy.$("#"+aStar.path[k].id()).data().weight);
                    var current_weight = cy.$("#"+aStar.path[k].id()).data().weight;
                    current_weight++;
                    // cy.$("#"+aStar.path[k].id()).data.weight += 1;
                    cy.$("#"+aStar.path[k].id()).json({"data":{"weight":current_weight}});
                    cy.$("#"+aStar.path[k].id()).json({"data":{"label":current_weight}});
                    // console.log(cy.$("#"+aStar.path[k].id()).data());

                }
            }

      }
    }





}
}

