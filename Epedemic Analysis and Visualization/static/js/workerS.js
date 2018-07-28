var j = 0;
var k;
this.onmessage = function (event)
 {
    k = event.data;
    while( j < k)
    {
      postMessage(j);

      j++;

    }    
}


